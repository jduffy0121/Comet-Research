#Program to run a single .yaml file or an array of .yaml files
#to get results for the vectorial model.
#
#Author: Jacob Duffy
#Version: 6/30/2022

import FileCreator
import UIVariables

#Method def for converting between km and astro units
def unitConvert(dataIn):
    return

#Method def for getting the output results for the vectorial model
def singleFileRun(fileName):
    file = open(fileName, 'r')
    result = str(file.read())
    file.close()
    return result

#Method def for taking an array of .yaml files and getting the output results
def multiFileRun(fileArray):
    if (UIVariables.FileInputs == False):
        return
    fileArray = []
    fileArray = UIVariables.FileArray
    index = 0
    while(index < len(fileArray)):
        singleFileRun(fileArray[index])
        index += 1

#Method def for running the program manually (ie: all input is done by user)
def runManualProgram():
    FileCreator.createDictionary()
    FileCreator.newFile()
    singleFileRun('pyvectorial.yaml')

#Method def for running the program with file inputs
def runFileProgram():
    multiFileRun(UIVariables.FileArray)
