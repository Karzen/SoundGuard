#The part used for file interaction

import soundguard_data as sdata
import os

def checkDataFilesExist(): #Checking if all files exists, and creates them if they dont
    for file in sdata.dataFiles:
        if not os.path.isfile(file):
            f = open(file, "w")
            f.close()

def writeListToFile(filename, lst, mode="w"): #Saving a list to a file
    file = open(filename, mode)
    for item in lst:
        file.write(str(item) + "\n")
    file.close()

def loadListFromFile(filename):#Loading a list to a file
    if os.path.isfile(filename):
        file = open(filename, "r")
        lst = file.read().split("\n")
        file.close()
        del lst[len(lst)-1]
        return lst
    return None

def removeElementFromFile(filename, element):#Removing a single element from a file containing a list
    if os.path.isfile(filename):
        file = open(filename, "r")
        lst = file.read().split("\n")
        try:
            del lst[0]
            lst.remove(element)
        except:
            pass
        file.close()
        writeListToFile(filename, lst)
        
def addElementToFile(filename, element): #Adding a single element to a file containing a list
    if os.path.isfile(filename):
        file = open(filename, "r")
        lst = file.read().split("\n")
        del lst[0]
        if element not in lst:
            lst.append(element)
            file.close()
            writeListToFile(filename, lst)
        else:
            file.close()

def writeModesToFile(filename, modes , mode="w"): #Saves the functioning modes of the app into a file
    file = open(filename, mode)
    for mod in modes:
        for times in mod:
            for time in times:
                file.write(str(time) + "|")
        file.write("^")
    file.close()

def loadModesFromFile(filename):
    file = open(filename, "r")
    modes = file.read().split("^")
    del modes[len(modes)-1]
    output = []
    index = 0
    for mod in modes:
        mod = mod.split("|")
        output.append([ [ int(mod[0]), int(mod[1]), int(mod[2]) ], [ int(mod[3]), int(mod[4]), int(mod[5]) ]])
    return output

def saveBoolArrayToFile(filename, array, mode="w"): #Saves a list containing only booleans to a file
    string = ""
    for bol in array:
        if bol:
            string += "1"
        else:
            string += "0"
    file = open(filename, mode)
    file.write(string)
    file.close()

def loadBoolArrayFromFile(filename):
    array = []
    file = open(filename, "r")
    string = file.read()
    file.close()
    for char in string:
        if char == "1":
            array.append(True)
        else:
            array.append(False)
    print("Prior")
    print(array)
    return array



