"""
buildMarkDownTOC.py

Notepad++ python script for inserting a table of contents into a markdown document.

Requires that the "Python Script" plug-in be installed.  Once Python Script is installed, store this script into the C:\Users\<username>\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts directory.  Run the script by opening the tab that contains the markdown document and then navigating to, and running, Plugins/Python Script/Scripts/buildMarkdownTOC.

The markdown file must have two horizontal rule lines (-----------------); this script will generate a table of contents and place it between the two horizontal rule lines, replacing whatever was there before (This is how an existing table of contents sitting between horizontal rules can be updated).

The script prompts for the number of levels for the table of contents. This defaults to 2.

   Author:   Mike DW
   Date:     2020-08-02
"""

def main():
    startPos,endPos = getTOCStartAndEnd()
    if (startPos < 0 or endPos < 0):
        notepad.messageBox('ERROR: markdown file needs at least 2 horizontal rule lines (^--------)')
        return
    startLine = editor.lineFromPosition(startPos)+1
    endLine = editor.lineFromPosition(endPos)
    numLevels = promptValue(sInfoText = 'Specify number of TOC levels (between 2 and 6):' ,
                           sTitleText = 'This script will build/replace a table of contents between lines '+str(startLine)+' and '+str(endLine),
                           sDefaultVal = 2,
                           iMinVal = 2,
                           iMaxVal = 6,
                           sRangeError = 'TOC levels value must be between 2 and 6',
                           bRepeatPrompt = True)
    if numLevels == None:
        return
    deleteLines(startPos,endPos);
    headings,levels = getHeadings()
    TOCEntries = headingsToTOC(headings,levels,numLevels)
    insertTOC(startPos,TOCEntries)

def deleteLines(startPos,endPos):
    lengthDelete = endPos-startPos
    editor.deleteRange(startPos,lengthDelete)
    

def getHeadings():
    headings = []
    levels = []
    editor.gotoPos(0)
    matches = []
    def match_found(m):
        matches.append(m.span(0))
    editor.research('^#',match_found)
    for startEnd in matches:
        heading = editor.getTextRange(startEnd[0],editor.positionFromLine(editor.lineFromPosition(startEnd[0])+1)-2)
        pos = 0
        level = 0
        for char in heading:
            if (char == '#'):
                level = level+1
            if (char != '#' and char != ' '):
                break
            pos = pos + 1
        heading = heading[pos:len(heading)] 
        levels.append(level-1)
        headings.append(heading) 
    return headings,levels

def headingsToTOC(headings,levels,numLevels):
    TOCEntries = []
    for headingNum in range(len(headings)):
        hyperlink = '#'
        for a in headings[headingNum]:
            if a.isalnum() or a == '_':
                hyperlink = hyperlink+a
            if a == ' ' or a == '-':
                hyperlink = hyperlink+'-'
        tocLine = '';
        if levels[headingNum] == 0 or levels[headingNum] > numLevels:
            headingNum = headingNum + 1
            continue
        for i in range(1,levels[headingNum]):
            tocLine = tocLine + '\t'
        tocLine = tocLine + '+ ['
        if levels[headingNum] == 1:
            tocLine = tocLine + '**'+headings[headingNum]+'**'
        else:
            tocLine = tocLine + headings[headingNum]
        tocLine = tocLine + '](' + hyperlink.lower() + ')'
        TOCEntries.append(tocLine)  
    return TOCEntries

def insertTOC(startPos,TOCEntries):
    insertPos = startPos
    editor.insertText(insertPos,'-----------------------\r\n')
    insertPos = insertPos + len('-----------------------\r\n')
    editor.insertText(insertPos,'## Table of Contents\r\n')
    insertPos = insertPos + len('## Table of Contents\r\n')
    for tocLine in TOCEntries:
        editor.insertText(insertPos,tocLine+'\r\n')
        insertPos = insertPos + len(tocLine+'\r\n')
    editor.insertText(insertPos,'  \r\n')
    insertPos = insertPos + len('  \r\n')
    editor.insertText(insertPos,'-----------------------\r\n')

def getTOCStartAndEnd():
    editor.gotoPos(0)
    matches = []
    def match_found(m):
        matches.append(m.span(0))
    editor.research('^----',match_found)
    startPos = -1
    endPos = -1
    if len(matches) > 0:
        startPos = matches[0][0]
    if len(matches) > 1:
        endPos = editor.positionFromLine(editor.lineFromPosition(matches[1][0])+1)
    return startPos,endPos
    
def promptValue(sInfoText, sTitleText, sDefaultVal, iMinVal, iMaxVal, sRangeError, bRepeatPrompt):
   while True:
      sNewVal = notepad.prompt(sInfoText, sTitleText, sDefaultVal)
      if sNewVal == None:
         return None

      try:
         iNewVal = int(sNewVal)
         if iMinVal <= iNewVal <= iMaxVal:
            return iNewVal
         else:
            raise
      except:
         notepad.messageBox(sRangeError + '.\n\nYou specified: ' + sNewVal +
                              '\n\nPlease specify a number between ' + str(iMinVal) + ' and ' + str(iMaxVal) + '.',
                              'Specified value is out of range')
         if not bRepeatPrompt:
            return None

main()
