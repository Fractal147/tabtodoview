# tabtodoview is a fork of the todo.txt format for easier handling of nested tasks
Made by Andrew Witty

Designed to be used as an all-in-one task list parser and sorter for text-based task management.

Tabbed indents are used to structure subtasks in a YAML or python like way that is very fast to type, and this is the main change from plain todo.txt format

The tree of tasks is then parsed, sorted, and presented by the script here, typically first by priority, then due date, then file location.
- So highest priority things will always be listed further up than lower/unlisted ones, but otherwise an untagged list's order will be maintained

Additionally, based on some tags, some shortlists are presented at the top of the output file.


## Main change from todo.txt
- Subtasks are defined by having an extra indent at the start of the line
- A subtask's parent is the lowest listed line with fewer indents
- Whitespace only lines (tabs and spaces only) are ignored in indents, sorting, and output
- Subtasks are always be listed below their parent task after any sorting
- - i.e. hierarchical sort based on indent level.

## Example

    (C) Example Main task 1
    	Example subtask 1a
    	(A) Example subtask 1b
    		(Z) Example subsubtask 1ba
    		(E) Example subsubtask 1bb
			x (A) done subtask 1bc
    		Example subsubtask 1bd
    	(F) Example subtask 1c
    (A) Example main task 2
    n example note
        subtask of note
            subsubtask of note
    x n example note and done
        subtask of done note
    x (B) Done task of some kind 3
        Not done subtask 3a

becomes after sorting

    (A) Example main task 2
    (C) Example Main task 1
    	(A) Example subtask 1b
    		(E) Example subsubtask 1bb
    		(Z) Example subsubtask 1ba
    		Example subsubtask 1bd
    	(F) Example subtask 1c
        Example subtask 1a
        Not done subtask 3a


## Extra tags
- +do is added to a shortlist, for day-to-day task management
- +inperson is added to a shortlist, for planning which work needs physical presense
- due:yyyy-mm-dd is used as the due date sort key
- 'x' at the start of the line (standard for done tasks) means it will not be output
- n or 'x n' at start of line counts the task and subtasks as a note
- - notes and their subtasks are not written out in the end file.
- - Use as a more correct way of adding notes to the todo list.

## Output listings
All listings are configurable in the top section of the script:
- includes relevant parameters
- includes whether they are output or not
- includes in what order they are output
All Flagged +do subtask oneliners and line numbers, in priority>due_date>file order:
 - A convenient list for doing manual task management 
 - (e.g. add +do to the tasks you want to do this hour/day/sprint)
All tasks due from yesterday to tomorrow with parent tasks, and subtask tree
- A list of those tasks due within certain days (inclusive) of the script running
- Output will include real dates defined - can be extended.
- Option to skip weekends in the day counting (so that 'one day forward from friday' gives the monday)
Most (over)due n tasks with parent tasks, subtask tree, and line numbers
- A listing with context of the most overdue 5 tasks
- Sorted by due date, then priority, then file location
All Flagged +inperson subtask onliners and line numbers, in priority>due_date>file order
- A convenient list for another tag, for things with mixed working from home or in office.
- All open tasks, sorted by priority tag (then due date, then file order):
- - Just a complete list of the whole file.

## Usage
- Adjust configuration options at the top of the tabtodoview.py script or accept defaults
- Run tabtodoview with the text file input, and it generates the view file under [inputname]_ttv

### Command line:

    python3 TABTODOVIEW inputfile.txt
	
## Extra
- The included .xml file is a UML colour scheme for notepad++, that presents reasonably nicely.

