# Changelog
All notable changes to this project will be documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),


## [Unreleased]
- Further options for selecting indent character
- Helpful parsing error output in separate file
- Possibly add settings section for number of lines in the most due/ +do tag....
- Warn if there's impossible jumping down in indent level (by more than one at a time)
- - As of 0.6.0 it will indent sensibly where possible, limiting to one at a time

## [0.8.0] - 2021-06-30
### Added
- Section for tasks due today +/- 1 days
- Configuration flags in script to adjust which sections are displayed.
- Configuration flags/globals to adjust parameters of sections.
### Changed
- Readme changes
- - Output sections section
- - Extra flags returned to design intent.
- - Minor wording changes in introduction
- Changes in task list titles for consistency.


## [0.7.0] - 2021-04-21
### Changed
- Put line numbers on all lines of output
- - Enables looking up line number in original file easily
- - Defaults to 4 digits, though if input file >9999 lines it will use 5 digits etc.
### Added
- Flags at top of script to modify when line numbers are printed
- - Only for main and overdue sections


## [0.6.2] - 2021-03-26
### Fixed
- lines within a note block are now ignored correctly.
- - for +do and for due:yyyy-mm-dd tags

## [0.6.1] - 2021-03-23
### Changed
- Added blank lines to output of date sorted tasks for easier viewing

## [0.6.0] - 2021-03-15
### Fixed
- Sorting error linked to empty line followed by whitespace lines, from 0.3.0
- - mainly by preventing empty lines having subtasks
### Changed
- Tweaked internal line numbering to start at line 1
- added debug flags at start of script to print extra info
- refactored sorting logic in read_in to be clearer
- used indentlevel instead of tabcount in read_in to be less affected by impossible indents

## [0.5.1] - 2021-03-15
### Fixed
- Removed sorting behaviour from notes

## [0.5.0] - 2021-03-15
### Changed
- Added 'n' start of line character to mark lines (and children) as notes to skip output
- note child note marking continues also in special case of 'x n'
- Fixed changelog dates

## [0.4.0] - 2021-02-05
### Changed
- Tided printed text
- added line numbers to top sections

## [0.3.0] - 2021-01-05
### Added 
- Add 'Most due' section at top with top 5 trees based on oldest due:yyyy-mm-dd date.
- Add '+do' section at top with lines only in same order with '+do' flag in
- Added various helper functions to do parsing of the tree into lists

### Changed
- Clarified comments

### Fixed
- Only indent by tabs at start of line
- Ignore whitespace lines in indenting logic

## [0.2.0] - 2020-08-12
### Changed
- Made script non-interactive

## [0.1.0] - 2020-08-12
### Added
- Created initial version

