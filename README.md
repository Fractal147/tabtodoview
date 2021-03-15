# tabtodoview is a fork of the todo.txt format
Made by Andrew Witty

Designed to be used as an all-in-one task manager

Essentially the input text file delimits projects by indents, forming a tree.

Then they are sorted and presented, for instance on priority, or due date.

Additionally, some can be added to a separate toplist based on the usual +tags

## Change from todo.txt
- Subtasks are defined by having an indent at the start of the line
- A subtask's parent is the lowest listed line with fewer indents.
- Subtasks must always be listed below their parent task after any sorting

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
	x n example note
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
- +do is added to a list on top, for day-to-day task management
	All +do flagged subtasks are listed as one liners at top of file
	(in the priority>due_date>file location order)
- due:yyyy-mm-dd is used as the due date sort for the second section
	Top 5 oldest dated tasks, their children, their parents are displayed
	(in due date>priority>file location order)
- +inperson is the third section, for those WFHers
	All +inperson flagged subtasks are listed as one liners
	(in the priority>due_date>file location order)
- n or 'x n' at start of line counts the task as a note
- - notes and their subtasks are not written out in the end file.
- - Usage as a more correct way of adding notes to the todo list.

## Usage
 - Run tabtodoview with the text file input, and it generates the view file under [inputname]_ttv

### Command line:

    python3 TABTODOVIEW inputfile.txt

