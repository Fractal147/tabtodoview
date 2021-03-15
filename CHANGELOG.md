# Changelog
All notable changes to this project will be documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),


## [Unreleased]
- Further options for selecting indent character
- Helpful parsing error output in separate file
- Possibly add settings section for number of lines in the most due/ +do tag....
- Warn if there's impossible jumping down in indent level (by more than one at a time)
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

