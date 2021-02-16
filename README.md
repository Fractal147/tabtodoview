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
    		Example subsubtask 1bc
    	(F) Example subtask 1c
    (A) Example main task 2

becomes after sorting

    (A) Example main task 2
    (C) Example Main task 1
    	(A) Example subtask 1b
    		(E) Example subsubtask 1bb
    		(Z) Example subsubtask 1ba
    		Example subsubtask 1bc
    	(F) Example subtask 1c
    	Example subtask 1a


## Usage
 - Run tabtodoview with the text file input, and it generates the view file under [inputname]_ttv

### Command line:

    python3 TABTODOVIEW inputfile.txt

