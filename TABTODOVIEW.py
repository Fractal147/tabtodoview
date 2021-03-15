#Todo viewer
#Andrew Witty
#Runs once, and interactive?

#Desired stuff - original brief v0.1: 
# present the todo sorted by position in file. then due date, then priority of first tasks, 
#and where subtasks defined by indents are present...
#display the highest priority topmost,
#then due date order topmost,
#then original file order.
#and subtasks of subtasks and so on. Retain the indent.
#Done stuff - don't display.
#whitespace lines - don't display


##Changelog now separate file, with planned changes, features, fixes.



import sys
import os
from operator import itemgetter
import re
print("Python Version is:", sys.version)
print("Script name is", sys.argv[0])
print("Arguments given:" , sys.argv[1:])

print_debug_indent_levels = False ##prints at start of line
print_debug_parent_line_number = False ##prints at start of line. don't use with above.

#in_mem_buffer_file = ""
#flat_lines_dict_list = []

def tabtodoview(fn_in):
    f_in = open(fn_in, 'rt')
    f_out = open(fn_in+'_ttv', 'wt') ##overwrite mode?

    ##walk through the file line by line...
    ##with tab level reflecting whether to make a new list.

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
        outputDict = {'text': inputLine};
        outputDict['linenumber'] = linenum+1;
        
        
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
                outputDict['prio'] = prioLetter;
                #print(str(linenum) + inputLine + " has prio " + prioLetter)
            if re.search('\ due:\d{4}-\d{2}-\d{2}', workingLine):
                indexOfDate = workingLine.find(" due:")+5
                dueDate = workingLine[indexOfDate:indexOfDate+10]
                outputDict['due'] = dueDate;
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
        
        for cnt, line in enumerate(f_in):
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
            
            

            
    
            
        f_in.close()
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



    
    def sort_prio_due(a_list_of_dicts):
        ##this fails horribly when it does not have the key, damn.
        ##and does not like string indicies not being integers.
        due_sorted = sorted(a_list_of_dicts, key=itemgetter('due') )#, reverse=True)
        prio_due_sorted = sorted(due_sorted, key=itemgetter('prio') )#, reverse=True)
        ##wi
        ##TEMPORARY...just prio only
        #prio_due_sorted = sorted(a_list_of_dicts, key=itemgetter('prio') )
        return prio_due_sorted

    def recursive_sort(a_dict):
        
        #for every dict that has the subslist
        #operating on master dict
        if 'subslist' in a_dict:
            #print("sorting ..." + a_dict['text'])
            a_dict['subslist'] = sort_prio_due(a_dict['subslist'])
            for d in a_dict['subslist']:
                d = recursive_sort(d)
        return a_dict
    

    def recursive_write(a_list_of_dicts):
        #for every dict that has the subslist
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
                            f_out.write(d['text'])
                                    
            if 'subslist' in d:
                recursive_write(d['subslist'])
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


    raw_dict = read_in(f_in)
    #print(raw_list)
    
    #input("Read In Fully, enter to continue")
    
    sorted_dict = recursive_sort(raw_dict) ##also probably sorts raw_dict to tbf
    #masterDict = recursive_sort(raw_list)
    #input("Sorted, enter to continue")
    #print (sortedListOfDicts)
    
    

    ##Make a flat version of the text list, so no 'subslist'
    #list_children_from_parent(sorted_dict) should do it!
    #Which can't be easily depth traversed (printed) since it links to itself
    ##but can always follow upwards

    ##Place to add extra features to the top of the file

    #Seach for '+do' flags....
    ##intelligent would be to display them as indented if they are subtasks, else new line
    ##Hmm, to do that needs (At least)the original dict per line - then can follow the tree up
    ##to sort those...needs a flat list of all line dicts.
    flag_do = "+do"

    #sorted_flat_list = sort_prio_due(flat_lines_dict_list)
    sorted_flat_list = list_children_from_parent(sorted_dict)
    f_out.write("*** All Flagged "+flag_do+" subtask oneliners and line numbers, in priority>date>file order:\n")
    for d in sorted_flat_list:
        if not ('isdone' in d or 'iswhitespace' in d or 'isdone' in d):
            if flag_do in d['text']:
                f_out.write(str(d['linenumber']).zfill(4))
                f_out.write(" ")
                f_out.write(d['text'].lstrip("\t"))
    f_out.write("\n\n")


    #Seach for top 5 outdated tasks....
    ##looking for a sorted list, based on due date primarily (then priority, then file order), ignoring indents, ingoring whitespace
    ##would be nice perhaps to be able to keep indents for display

    #present with parents up to head, and children.

    number_of_oldest_tasks = min(5, len(sorted_flat_list))
    due_sorted_flat = sorted(sorted_flat_list,  key=itemgetter('due') )#, reverse=True)
    ##conveniently, done tasks don't have due date saved here
    f_out.write("*** Most (over)due " + str(number_of_oldest_tasks) + " tasks with parent tasks, subtask tree, and line numbers:\n")
    for d in due_sorted_flat[:number_of_oldest_tasks]:
        #f_out.write("\t"+ d['text'].lstrip('\t') ) ##works fine for one line/task
        ##for d2 in list_elders_from_child(d): ##only lists higher tasks
        if not d['due'] == "ZZZ": ##default for anything without due:date
            for d2 in list_all_family_from_child(d):
                ##f_out.write("\t")
                #print(d2)
                if not ('isdone' in d2 or 'iswhitespace' in d2 or 'isdone' in d2):
                    #if d2['tabCount'] == 0: #for the first line only
                    f_out.write(str(d2['linenumber']).zfill(4))
                    f_out.write(" ")
                    #else:
                    #f_out.write("\t")
                    f_out.write(d2['text'])
    f_out.write("\n\n")
       
    #Seach for '+inperson' flags....
    ##Display as one line tasks without indents
    ##to sort those...needs a flat list of all line dicts.
    flag_ip = "+inperson"
    #sorted_flat_list = sort_prio_due(flat_lines_dict_list)
    ##sorted_flat_list = list_children_from_parent(sorted_dict) ##already sorted above
    f_out.write("*** All Flagged "+flag_ip+" subtask onliners and line numbers, in priority>date>file order:\n")
    for d in sorted_flat_list:
        if not ('isdone' in d or 'iswhitespace' in d or 'isdone' in d):
            if flag_ip in d['text']:
                f_out.write(str(d['linenumber']).zfill(4))
                f_out.write(" ")
                f_out.write(d['text'].lstrip("\t"))
    f_out.write("\n\n")



    #Write out the rest of the list to f_out
    f_out.write("*** All open tasks, sorted by priority tag (then due date, then file order):\n")
    recursive_write(sorted_dict['subslist'])


    
    f_out.close()
    print("Done!")

    return 





if len(sys.argv) <= 1: 
    ###print ("ERROR: No arguments given")
    ###exit()
    print("No file to view given, defaulting to TODOLIST1")
    #infilename = input("What file (default TODOLIST1)") or "TODOLIST1"
    infilename="..\TODOLIST1"
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
