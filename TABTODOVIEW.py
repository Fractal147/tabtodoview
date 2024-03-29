#Todo viewer
#Andrew Witty

##CHANGELOG.md has master list of planned changes, features, fixes.

import sys
import os
from operator import itemgetter
import re
import math ##used for file number counting
from datetime import datetime ##used for "today's" date feature
from datetime import timedelta ##used for relative date
print("Python Version is:", sys.version)
print("Script name is", sys.argv[0])
print("Arguments given:" , sys.argv[1:])


###CONFIGURATION###
print_line_numbers_main_list = True ## Prints line numbers at start of 'main' section
print_line_numbers_datesorted_trees = True ## Prints line numbers at start of 'most overdue' and 'due near today' section
print_line_numbers_flagged_lists = True ## Line numbers on e.g. +do and +inprogress lists

######Output listing configuration######

##Comment out a line to disable that listing
##Reorder to ... reorder.
##Change parameters to adjust

def print_output_lists():
    print_flagged_list(flag_text="+do") 
    print_due_recently_list(days_back = 1, days_forwards = 1, count_weekdays_only = True) # e.g 1,1, = yesterday to tomorrow
        # count_weekdays_only means it only counts weekdays - hence 'next day' from Friday is Monday (anything due on the weekend is included too in the outputs)
    print_over_due_top_n_list(number_of_oldest_tasks=5)
    ###example_disabled_list()
    print_flagged_list(flag_text="+inperson") 
    print_all_open_tasks_list()
    end_of_list_footer()
    return



###DEBUG FLAGS###
print_debug_indent_levels = False ##prints at start of line
print_debug_parent_line_number = False ##prints at start of line. don't use with above.



def tabtodoview(fn_in):
    f_in = open(fn_in, 'rt',encoding="utf-8") 
    #The encoding can be done wrong, e.g. this snippet gives cp1252 in some cases
        #f_in = open(fn_in, 'rt')
        #print(f_in.encoding)

    global f_out
    f_out = open(fn_in+'_ttv', 'wt') ##overwrite mode?


    ######Read in the file into a dictionary:################
    raw_dict = read_in(f_in)
    f_in.close()
    #input("Read In Fully, enter to continue")
    
    ###Sort it nicely in priority>due_date>file_order
    global sorted_dict
    sorted_dict = recursive_sort(raw_dict)  ##May also actually sort the raw_dict, unsure.
    #input("Sorted, enter to continue")
    
    ##Make a flat version of the text list, so no 'subslist's - every line is included here 
    ##Note that still from a 'line' here it's easy to reconstruct the sorted tree from sorted_dict, and the links
    ##still contains notes, whitespace, and done stuff.
    sorted_flat_list = list_children_from_parent(sorted_dict) 
    
    ##remove all notes since they still can have tags, priorities, and due dates which need ignoring
    global sorted_flat_list_nonotes
    sorted_flat_list_nonotes = [
        i for i in sorted_flat_list if not(i.get('isnote',0) == 1)
        ] 

    ##Process line numbering formats
    max_line_number = len(sorted_flat_list)
    global num_digits_for_line_num
    num_digits_for_line_num = math.log(max_line_number,10)
    num_digits_for_line_num = math.ceil(num_digits_for_line_num)

    ##iterate over the list of output functions to give output file.
    print_output_lists()

    f_out.close()
    print("Done!")

    return  ##end of main function


#in_mem_buffer_file = ""
#flat_lines_dict_list = []


    #pseudocode for importing...
##    file_listed = new.list
##    line_num =0
##    tabcount_previousline =-1
##    for line in f_in:
##        line_num += 1
##        if is_whitespace: skip line
##        tabcount =  tabsatstart(line)
##        prio = letter_to_number(letter_in_brackets(line))
##        linenumber = line_num
##        isdone = is_ws_x_space(line)
##        text_content = line
##
##        if tabcount = tabcount_previousLine:
##            ##know that info is to be added as subset
##            ##if not done, make previous head tagged as head
##            ##and then append this dict to it's list of subs
##
# 
    
##want a really nice recursive function here so it's nice and compact to code.
#conceptually needs to recurse in if there's another indent
#recurse out  by the correct number of levels if there's less
#or just work on it every time based on indent level...
#linked list - so each dict knows it's parent dict?
#at least this function needs to know all the way up.
##Not sure how to do this sort of recusive access.
   
##        line_num += 1
##        if is_whitespace: skip line
##        tabcount =  tabsatstart(line)
##        prio = letter_to_number(letter_in_brackets(line))
##        linenumber = line_num
##        isdone = is_ws_x_space(line)
##        text = line
##          iswhitespace = line.isspace()
##        isnote
    
def parse_line(inputLine, linenum):
    outputDict = {'text': inputLine}
    outputDict['linenumber'] = linenum+1
    
    
    outputDict['prio']= "ZZ"
    outputDict['due'] = "ZZZ" ##placeholders

    workingLine = inputLine.lstrip('\t')
    #outputDict['tabCount'] = inputLine.count('\t') ##BUGGY IT MUST MUST ONLY DO LEFT SIDE
    outputDict['tabCount'] = len(inputLine) - len(workingLine)
    
    if ( inputLine.isspace() or not inputLine ): ## blank lines are falsey
        outputDict['iswhitespace']=1
        return outputDict #and skip the rest.
    

    
    ##just do regex matches
    # '^x\ ' for 'x '
    # '(\w)' for priority
    # 'due:' for due then trimming
    #x (A)
    #0123456789
    
    #search for note tag at the start of line.
    if re.search('^n\ |^x\ n\ ', workingLine):
        ##This line is a note, and it's children are too.
        outputDict['isnote']=1
    
    if  re.search('^x\ ', workingLine):
        #print(str(linenum) + inputLine + " Is WS")
        outputDict['isdone'] =1
        ##flag priority of task as lowest of the low...skipped for v3
        #outputDict['prio'] = "ZZZ"

    if not ('isdone' in outputDict or 'isnote' in outputDict):
    ## done or note items can't have a high priority or due
        if  re.search('\(\w\)', workingLine):
            prioLetter = workingLine[workingLine.find("(")+1]
            outputDict['prio'] = prioLetter
            #print(str(linenum) + inputLine + " has prio " + prioLetter)
        if re.search('\ due:\d{4}-\d{2}-\d{2}', workingLine):
            indexOfDate = workingLine.find(" due:")+5
            dueDate = workingLine[indexOfDate:indexOfDate+10]
            outputDict['due'] = dueDate
            ##outputDict['hasDueDate'] = 1
            #print(str(linenum) + inputLine + " has duedate" + dueDate)

    

    #if '(#)' in workingLine:
        #prionum = line.split('(')
        #outputDict['prio':
    
    
    
    
##        outputDict ={
##            'text': test
##            'line': linenum,
##            'prio': 'abc',
##            'due': '2020-01-01 ,
##            'subslist' : [],
##            'parentDict': {}
##            'indentCount': counttabs
##            };
    
    
    return outputDict



def read_in(in_file_handle):
    headDict = {}
    headDict['subslist'] = []
    headDict['tabCount'] = -1 ##so anything in the list has tabcount of 0
    headDict['indentlevel'] = -1 ##so anything in the list has indent of 0
    headDict['prio'] = "ZZ"
    headDict['due']= "ZZZ"
    headDict['text'] = "Head"
    headDict['linenumber'] = -1

    parent_dict = headDict
    previous_good_dict = headDict
    #headDict.subslist[0].subslist[0].subslist[0].subslist....

    parentIndentLevel = -1 ##simple 1 for each indent.
    
    #global flat_lines_dict_list ##for adding to too.

    ##ok, this is going to work best with a linked list.
    #can path downwards easily due to structure.
    #But each dict should reference the dict above it
    #so each and every dict? I guess knows the parent dict.
    
    for cnt, line in enumerate(in_file_handle):

        #print(str(cnt) + " : " + line)        
        thisLineDict = parse_line(line,cnt);
        #thisLineDict['grandparentDict']
        #flat_lines_dict_list.append(thisLineDict)

        ##should ignore indents if whitespace, and store them as if just other tasks of the same orde
        ##This could go wrong if it's a new master task, then whitespace, then tasks.
        ##So care with parents - successive whitespace lines are all treated as subtasks of previous
        ##and a whitespace line can't become a parent.

        if (thisLineDict.get('iswhitespace', 0) ==1):
            ##it's whitespace, so treat it as indented
            lineIndentLevel = parentIndentLevel+1
        else:
            lineIndentLevel = thisLineDict['tabCount']
        
        ##for going deeper, it must be a subtask of the previous line 
        if lineIndentLevel > (parentIndentLevel+1):
            ##need to go deeper, make subslist in previous dict
            previous_good_dict['subslist'] = []
            parent_dict = previous_good_dict ##previous_good_dict is last non-whitespace dict.
            #never trust tabcount since it may jump by >1 deep.
            parentIndentLevel = parent_dict['indentlevel']
            lineIndentLevel = parentIndentLevel+1
            
        ##this bit was misorting lines prior to 0.6.0, particularly when whitespace involved.

        #now never entered by whitespace lines!
        ##for going shallower, repeat until it has a parent less indented than it
        while lineIndentLevel <= parentIndentLevel: 
            ##need to go shallower, 
            parent_dict  = parent_dict['parentDict'] ##parent now grandfather
            parentIndentLevel = parent_dict['indentlevel']
        
        #if not(lineIndentLevel == workingIndentLevel):
            #print("error, could not indent to " + str(lineIndentLevel) +" got to " + str(workingIndentLevel))
        ##it'll get stuck in the while loops surely though.
        
        #recursively propogate note property.
        if parent_dict.get('isnote', 0)==1:
                thisLineDict['isnote']=1
        #store indent level
        thisLineDict['indentlevel'] = lineIndentLevel
        #store parent relation
        thisLineDict['parentDict'] = parent_dict
        #add this line to approprite list.
        parent_dict['subslist'].append( thisLineDict)
        
        #only if not whitespace can it be stored
        if (thisLineDict.get('iswhitespace', 0) ==0):
            previous_good_dict = thisLineDict
        

        
    
    return headDict#['subslist']

#Are priorities per task or global? Can add tags of course.
        #but both ways make sense....
#Presentation of high priority subtasks must also print context - so all head tasks above them
        
#list of dicts - end up needing to print out that list...

##1task1
##2
##3task2
##4    task2a due:2020-07-29
##5        task2ai
##6        x (C) task2aii
##7        (B) task2aiii
##8    (A) task2b 
        
##want it stored as listOfDicts
    #line = original file line, used for sorting perhaps?
    #subs=  count of direct sublines (not second order subtasks) could be len (subslist), or nothing...
        #may depreciate and just have subslist length.
    #prio= priority letter OR nothing?
    #due = due date in text
    #isdone = 1 or nothing
    #subslist = LIST of dicts
    #iswhitespace = 1 or nothing
        #listofDicts=[dict1, dict2, dict3]
    #so example above goes to:
        #dict1=     {line:1, text="task1"}
        #dict2=     {line:2, text="     ", iswhitespace:1}
        #dict3 =    {line:3, text="task2", subs:2, subslist:[dict2.1, dict2.2]}
            #dict3.1 =  {line:4, text="task2a due:2020-07-29", due:"2020-07-29", subs:3, subslist:[dict3.1.1, dict3.1.2, dict3.1.3]}
                #dict3.1.1= {line:5, text="task2ai", subs:0}
                #dict3.1.2= {line:6, text="x (C) task2aii", prio:"C", isdone:1}
                #dict3.1.3= {line:7, text="(B) task2aiii", prio:"B" }
        #dict2.2 =  {line:8, text="(A) task2b", prio='A'}
    


##work through the sorting process perhaps?
##can sort simple easy lists of line numbers...
##but easier to sort whole structures conceptually.
    #so list of dicts
#https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
    
#from operator import itemgetter
#newlist = sorted(list_to_be_sorted, key=itemgetter('name'), reverse=True)
#Need to recursively do it too...


#Desired stuff - original brief v0.1: 
# present the todo sorted by position in file. then due date, then priority of first tasks, (last most important)
#and where subtasks defined by indents are present... Retain the indent.
#Done stuff - don't display.
#whitespace lines - don't display
#notes - don't display

    
def sort_prio_due(a_list_of_dicts):
    ##this fails horribly when it does not have the key
    ##and does not like string indicies not being integers.
    due_sorted = sorted(a_list_of_dicts, key=itemgetter('due') )#, reverse=True)
    prio_due_sorted = sorted(due_sorted, key=itemgetter('prio') )#, reverse=True)
    return prio_due_sorted

def recursive_sort(a_dict):
    #for every dict that has the subslist, descend.
    #dicts without a subslist - sort.
    #operating on master dict
    if 'subslist' in a_dict:
        #print("sorting ..." + a_dict['text'])
        a_dict['subslist'] = sort_prio_due(a_dict['subslist'])
        for d in a_dict['subslist']:
            d = recursive_sort(d)
    return a_dict


def recursive_write(a_list_of_dicts, line_num_digits = 0):
    #for every dict that has the subslist
    ##line_num_digits - number of digits to pad line numbers to. If 0, then don't print them.
    for d in a_list_of_dicts:
        ##At present it will write all lines that are not done
        # If a task above is complete, but subtasks not, they'll still be written
        # but orphaned, though in the right place
        if not('isdone' in d):
            if not('iswhitespace' in d):
                if not('isnote' in d):
                    if (print_debug_indent_levels):
                        f_out.write(str(d['indentlevel'])+d['text'])
                    if (print_debug_parent_line_number ):
                        f_out.write(str(d['parentDict']['linenumber'])+d['text'])
                    else:
                        if (line_num_digits):
                            f_out.write(str(d['linenumber']).zfill(line_num_digits))
                            f_out.write(" ")
                        f_out.write(d['text'])
                                
        if 'subslist' in d:
            recursive_write(d['subslist'], line_num_digits)
    return


def list_elders_from_child(child_dict):
    family_list =[]
    family_list.append(child_dict)
    while 'parentDict' in family_list[0]:
        family_list.insert(0, family_list[0]['parentDict'])
    return family_list[1:] ##as first one is always head

def list_children_from_parent(parent_dict):
    family_list=[]
    family_list.append(parent_dict)
    ##this needs to run recursively...
    ##else it will miss stuff that's not at end of list.
    ##or it just marches through in list order, one-by-one, adding new stuff afterwards
    listIndex = len(family_list) - 1 #start at the last one.
    while listIndex < len(family_list):
        if 'subslist' in family_list[listIndex]:
            #insert into family_list the whole subslist - slow and faffy, as only .extend works on iterables
            # list_afterwards = family_list[listIndex+1:] ##should be safe if list is 1 long
            # family_list = family_list[:listIndex+1] ##So it's now got only the first part of the list
            # family_list.extend(family_list[listIndex]['subslist'])
            # family_list.extend(list_afterwards) 
            family_list[listIndex+1:listIndex+1] = family_list[listIndex]['subslist']  ##python slicing is great - all lines above become this
        listIndex +=1

    return family_list

def list_all_family_from_child(child_dict):
    family_list =list_elders_from_child(child_dict)
    family_list.extend(list_children_from_parent(child_dict)[1:] ) ##as first one is child

    return family_list

#####OUTPUT LIST FUNCTIONS
#These pull directly from lists defined after reading (which will be in scope) (no problem as long as they don't modify)
##New list functions would have to go here.


global print_flagged_list
def print_flagged_list(flag_text):
    #e.g Seach for and display all +do flagged lines in a sorted flat list of all tasks

    #TODO: #intelligent would be to display them as indented if they are subtasks, else new line
    ##Hmm, to do that needs (At least)the original dict per line - then can follow the tree up
    
    f_out.write("*** All Flagged "+flag_text +" subtask oneliners")
    if (print_line_numbers_flagged_lists):
        f_out.write(" and line numbers,")
    f_out.write(" in priority>due_date>file_order:\n")
    
    
    for d in sorted_flat_list_nonotes:
        if not ('isdone' in d or 'iswhitespace' in d or 'isnote' in d):
            if flag_text  in d['text']:
                if(print_line_numbers_flagged_lists):
                    f_out.write(str(d['linenumber']).zfill(num_digits_for_line_num))
                    f_out.write(" ")
                f_out.write(d['text'].lstrip("\t"))
    f_out.write("\n\n")
    return


global print_over_due_top_n_list
def print_over_due_top_n_list(number_of_oldest_tasks):
    #Seach for top e.g. 5 outdated tasks....
    ##looking for a sorted list, based on due date primarily (then priority, then file order), ignoring indents, ingoring whitespace
    ##would be nice perhaps to be able to keep indents for display

    #present with parents up to head, and children.
    
    number_of_oldest_tasks = min(5, len(sorted_flat_list_nonotes))
    due_sorted_flat = sorted(sorted_flat_list_nonotes,  key=itemgetter('due') )#, reverse=True)
    ##conveniently, done tasks don't have due date saved here

    f_out.write("*** Most (over)due " + str(number_of_oldest_tasks) + " tasks with ")
    if(print_line_numbers_datesorted_trees): f_out.write("line numbers, ")
    f_out.write("parent tasks, and subtask tree:\n")
    
    for d in due_sorted_flat[:number_of_oldest_tasks]:
        #f_out.write("\t"+ d['text'].lstrip('\t') ) ##works fine for one line/task
        ##for d2 in list_elders_from_child(d): ##only lists higher tasks
        if not (d.get('due',"ZZZ") == "ZZZ"): ##default for anything without due:date
            for d2 in list_all_family_from_child(d):
                ##f_out.write("\t")
                #print(d2)
                if not ('isdone' in d2 or 'iswhitespace' in d2 or 'isnote' in d2):
                    #if d2['tabCount'] == 0: #for the first line only
                    if(print_line_numbers_datesorted_trees):
                        f_out.write(str(d2['linenumber']).zfill(num_digits_for_line_num))
                        f_out.write(" ")
                    #else:
                    #f_out.write("\t")
                    f_out.write(d2['text'])
        f_out.write("\n")
    f_out.write("\n")
    return

global print_all_open_tasks_list
def print_all_open_tasks_list():
    f_out.write("*** All open tasks ")
    if(print_line_numbers_main_list):
        f_out.write("and line numbers ")
    f_out.write("in priority>due_date>file_order:\n")

    if(print_line_numbers_main_list):
        main_list_num_digits = num_digits_for_line_num
    else:
        main_list_num_digits = 0

    recursive_write(sorted_dict['subslist'], main_list_num_digits)

    f_out.write("\n\n")
    return


global print_due_recently_list
def print_due_recently_list(days_back,days_forwards, count_weekdays_only  = False):
    ##calculate due date range from today:
    run_datetime = datetime.now()
    time_delta_1day = timedelta(days=1)

    #step through from today, day by day, until days_forwards weekdays have ocurred.
    weekday_count = 0
    max_date = run_datetime
    while (weekday_count < days_forwards):
        max_date += time_delta_1day
        if max_date.isoweekday() in range(1,6): ##adjust the range to say what days 'count'
            weekday_count +=1

    max_date = max_date.isoformat()[:10] ##full iso8601 timestamp, but cut off everything after the date

    #step back from today, day by day, until days_back weekdays have ocurred.
    weekday_count = 0
    min_date = run_datetime
    while (weekday_count < days_forwards):
        min_date -= time_delta_1day
        if min_date.isoweekday() in range(1,6): ##adjust the range to say what days 'count'
            weekday_count +=1

    min_date = min_date.isoformat()[:10] ##full iso8601 timestamp, but cut off everything after the date


    ##actually sort the data - may be more performant to trim first?
    due_sorted_flat = sorted(sorted_flat_list_nonotes,  key=itemgetter('due') )

    ##strip out ones where due date doesn't match or no due date
    ##Probably more performant ways to do this, given it's sorted
    due_sorted_flat_daterange = [
    i for i in due_sorted_flat if (  (i.get('due',"ZZZ") >=min_date) and (i.get('due',"ZZZ") <= max_date))
    ]
    
    
    f_out.write("*** Tasks due from " +min_date+ " to " + max_date + ", with ")
    if(print_line_numbers_datesorted_trees): 
        f_out.write("line numbers, ")
    f_out.write("parent tasks, and subtask tree:\n")
    for d in due_sorted_flat_daterange:
        #f_out.write("\t"+ d['text'].lstrip('\t') ) ##works fine for one line/task
        ##for d2 in list_elders_from_child(d): ##only lists higher tasks
        
        for d2 in list_all_family_from_child(d):
            if not ('isdone' in d2 or 'iswhitespace' in d2 or 'isnote' in d2):
                #if d2['tabCount'] == 0: #for the first line only
                if(print_line_numbers_datesorted_trees):
                    f_out.write(str(d2['linenumber']).zfill(num_digits_for_line_num))
                    f_out.write(" ")
                #else:
                #f_out.write("\t")
                f_out.write(d2['text'])
        f_out.write("\n")
    f_out.write("\n")

    return

global end_of_list_footer
def end_of_list_footer():

    f_out.write("*** End of file, generated on " + datetime.now().isoformat())

    return











if len(sys.argv) <= 1: 
    ###print ("ERROR: No arguments given")
    ###exit()
    print("No file to view given, defaulting to TODOLIST1")
    #infilename = input("What file (default TODOLIST1)") or "TODOLIST1"
    infilename=r"..\TODOLIST1"
    working_filename =  os.path.join( os.path.split(sys.argv[0])[0], infilename)
else:
    working_filename = sys.argv[1]


#n=0
#wait for break or for 'q'?
#while (n<1):

print("preparing to run")
tabtodoview(working_filename)
print("one run done")

#sleep(10000)

    
#exit()
