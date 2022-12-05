import string
import os
import re

# Global search function to search input string for a specific string and return the match.
# Only use where there is one match
def searchString(expres,string):
    temp = re.search(expres,string)
    if temp != None:
        temp = temp.group()
        return temp
    else:
        temp = ""
        return temp

# Uses the substitution function to replace specific strings of characters with no space
def removeJunk(expres,string):
    temp = re.sub(expres,"",string)
    return temp

# Replace periods with a space
def removePeriods(string):
    temp = re.sub("\."," ",string)
    return temp

# Replace a part of the input string with a new string
def replaceString(expres,new,string):
    temp = re.sub(expres,new,string)
    return temp

startDir = input("Enter the starting directory: ")
dir_list = []


for root, dirs, files in os.walk(startDir):
    for file in files:
        if re.search(r"^\.",file) == None:
            # Removes any string of characters enclosed in []
            noBrackets = re.sub("(\s\[[^\]]*\])\s|\[[^\]]*\]\s|(\[[^\]]*\])","", file)
            
            # Grabs the file extension from the file name
            exten = searchString(r"(\.([a-z0-9]+))$",noBrackets)

            # Removes junk at end of name starting from string like .1080p
            noJunk = removeJunk("\.[0-9]+[a-z]+.+",noBrackets)

            # Replace periods in string with periods
            extenCheck = searchString(r"(\.([a-z0-9]+))$",noJunk)
            # print("\n\nFiles extension is '" + exten + "'. Extension still in file is '" + extenCheck + "'. Original file was: " + file)
            if extenCheck == exten:
                noJunk = removeJunk(extenCheck,noJunk)
                noPeriods = removePeriods(noJunk)
            else:
                noPeriods = removePeriods(noJunk)
            
            # If string has a year in it, this will put it in parentheses and remove anything else that in between the year and the extension
            fileYear = searchString("[0-9][0-9][0-9][0-9]",noPeriods)
            if fileYear != "":
                noPeriods = replaceString(fileYear,"(" + fileYear + ")", noPeriods)
                noPeriods = removeJunk("(?<=\([0-9][0-9][0-9][0-9]\)).+",noPeriods)
            finalString = string.capwords(noPeriods)
            finalString = replaceString(searchString(r"[sS][0-9][0-9][eE][0-9][0-9]",finalString),searchString(r"[sS][0-9][0-9][eE][0-9][0-9]",finalString).upper(),finalString)
            testTemp = searchString(r"(?<=[sS][0-9][0-9][eE][0-9][0-9]).+",finalString)

            # If there is text after the season/episode string, add a space and dash after it 
            if (searchString(r"(?<=[sS][0-9][0-9][eE][0-9][0-9]).+",finalString) == "") & (searchString(r"[sS][0-9][0-9][eE][0-9][0-9]",finalString) != ""):
                finalString = replaceString(searchString(r"[sS][0-9][0-9][eE][0-9][0-9]",finalString),)
            # print("Old file name and path is: '" + root + "\\" + file +"'. New file name is: '" + finalString + exten + "'.")
        dir_list.append(os.path.join(root,file))



