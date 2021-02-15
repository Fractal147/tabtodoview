#Todo viewer
#Andrew Witty
#Runs once, and interactive?

#Desired stuff: present the todo sorted by priority of first tasks, then position in file.
#and where subtasks defined by indents are present...
#display the highest priority topmost,
#then due date order topmost,
#then original file order.
#and subtasks of subtasks and so on. Retain the indent.
#Done stuff - don't display.
#whitespace lines - don't display

import sys
import os
from operator import itemgetter
import re
print("Python Version is:", sys.version)
print("Script name/version is", sys.argv[0])
print("Arguments given:" , sys.argv[1:])


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
    
    def parse_line(inputLine, linenum):
        outputDict = {'text': inputLine};
        outputDict['linenumber'] = linenum;
        
        
        outputDict['prio']= "ZZ"
        outputDict['due'] = "ZZZ" ##placeholders

        workingLine = inputLine.lstrip('\t')
        #outputDict['tabCount'] = inputLine.count('\t') ##BUG IT MUST MUST ONLY DO LEFT SIDE
        outputDict['tabCount'] = len(inputLine) - len(workingLine)
        
        if inputLine.isspace():
            outputDict['iswhitespace']=1
            return outputDict #and skip the rest.
        

        
        ##just do regex matches
        # '^x\ ' for 'x '
        # '(\w)' for priority
        # 'due:' for due then trimming
        #x (A)
        #0123456789
        
        if  re.search('^x\ ', workingLine):
            #print(str(linenum) + inputLine + " Is WS")
            outputDict['isdone'] =1;
            outputDict['prio'] = "ZZZ"
        else: ## done items can't have a high priority or due
            if  re.search('\(\w\)', workingLine):
                prioLetter = workingLine[workingLine.find("(")+1]
                outputDict['prio'] = prioLetter;
                #print(str(linenum) + inputLine + " has prio " + prioLetter)
            if re.search('\ due:\d{4}-\d{2}-\d{2}', workingLine):
                indexOfDate = workingLine.find(" due:")+4
                dueDate = workingLine[indexOfDate:indexOfDate+10]
                outputDict['due'] = dueDate;
                #print(str(linenum) + inputLine + " has duedate" + dueDate)

        

        #if '(#)' in workingLine:
            #prionum = line.split('(')
            #outputDict['prio':
        
        
        
        
##        outputDict ={
##            'line': linenum,
##            'prio': 'abc',
##            'due':  ,
##            #'subslist' : [],
##            #parentDict: {}
##            'indentCount': counttabs
##            };
        
        
        return outputDict


    
    def read_in(in_file_handle):
        headDict = {}
        headDict['subslist'] = []
        headDict['tabCount'] = -1 ##so anything in the list has indent of 0
        headDict['prio'] = "ZZ"
        headDict['due']= "ZZZ"
        headDict['text'] = "Head"

        parent_dict = headDict;
        #headDict.subslist[0].subslist[0].subslist[0].subslist....

        workingIndentLevel = 0 ##simple 1 for each indent.
        listIndex = 0

        ##ok, this is going to work best with a linked list.
        #can path downwards easily due to structure.
        #But each dict should reference the dict above it
        #so each and every dict? I guess knows the parent dict.
        
        for cnt, line in enumerate(f_in):
            #print(str(cnt) + " : " + line)        
            thisLineDict = parse_line(line,cnt);
            #thisLineDict['grandparentDict']

            lineIndentLevel = thisLineDict['tabCount']
            ##ignore indents if whitespace though... Maybe?


            if lineIndentLevel > workingIndentLevel:
                ##need to go deeper, make subslist in previous dict
                previous_dict['subslist'] = []
                parent_dict = previous_dict
                listIndex =0
                workingIndentLevel = parent_dict['tabCount']+1
                

            while lineIndentLevel < workingIndentLevel:
                ##need to go shallower, 
                parent_dict  = parent_dict['parentDict']
                listIndex = len(parent_dict['subslist']) ##so now listIndex is poised in next free space.
                workingIndentLevel = parent_dict['tabCount']+1
            

            #if not(lineIndentLevel == workingIndentLevel):
                #print("error, could not indent to " + str(lineIndentLevel) +" got to " + str(workingIndentLevel))
            ##it'll get stuck in the while loops surely though.
            thisLineDict['parentDict'] = parent_dict;
            parent_dict['subslist'].append( thisLineDict);
           
            previous_dict = thisLineDict
            listIndex += 1
            

            
    
            
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
            ##todo - add an if is done then skip bit here
            ##for now if major task is done it skips all subs- must manuall reopen
            
            if not('isdone' in d):
                if not('iswhitespace' in d):
                    f_out.write(d['text'])
            
            if 'subslist' in d:
                recursive_write(d['subslist'])
                
            
            
        return

    raw_dict = read_in(f_in)
    #print(raw_list)
    
    #input("Read In Fully, enter to continue")
    
    sorted_dict = recursive_sort(raw_dict) ##also probably sorts raw_dict to tbf
    #masterDict = recursive_sort(raw_list)
    #input("Sorted, enter to continue")
    #print (sortedListOfDicts)
    recursive_write(sorted_dict['subslist'])
    
    f_out.close()
    print("Done!")

    return 





if len(sys.argv) <= 1: 
    ###print ("ERROR: No arguments given")
    ###exit()
    print("No file to view given")
    #infilename = input("What file (default TODOLIST1)") or "TODOLIST1"
    infilename="TODOLIST1"
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
