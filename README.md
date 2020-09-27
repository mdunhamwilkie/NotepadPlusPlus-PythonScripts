# NotepadPlusPlus-PythonScripts

This repository contains Python scripts that can be used with the Notepad++ Python Script plugin.

-----------------------
## Table of Contents
+ [**buildMarkdownTOC.py**](#buildmarkdowntocpy)
	+ [How it works](#how-it-works)
	+ [Installation instructions](#installation-instructions)
	+ [Sample markdown files](#sample-markdown-files)
  
-----------------------

## buildMarkdownTOC.py

This script is used to insert a table of contents into a markdown file.  The markdown file is assumed to have 
* one heading level 1 heading (the document title)
* two horizontal rules (lines containing three or more asterisks (***), dashes (---), or underscores (___) on the line by themselves)
The table of contents will be inserted between the two horizontal rules, removing any text that is already there.

### How it works

With the cursor positioned anywhere in the file, select menu item Plugins :arrow_right:  Python Script :arrow_right: Scripts :arrow_right: buildMarkdownTOC.
A pop-up will appear, asking you how many heading levels you want.  The default is 2 (heading levels 2 and 3).  Note that no table of contents lines are created for level 1 headings, as it is assumed that there is just one level 1 heading (i.e., the document title).

### Installation instructions

1. Add the Python Script plugin
	1. Select menu item Plugins :arrow_right: Plugins Admin...
	1. Search for and install Python Script
2. Copy the buildMarkdownTOC.py file to (on Windows 10)
`<C:\Users\<USERNAME>\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\buildMarkdownTOC.py>`

### Sample markdown files

The repository contains two sample files:

- buildMarkdownTOC_sample_before.md: a markdown file with the two horizontal rules required for this script to work.
- buildMarkdownTOC_sample_after_2Levels.md: the markdown file after the buildMarkdownTOC Python Script has been run, specifying **2** for the ***number of TOC levels***.