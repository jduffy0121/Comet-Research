#Program to run a single .yaml file or an array of .yaml files
#to get results for the vectorial model.
#
#Author: Jacob Duffy
#Version: 6/29/2022

import UIVariables
import numpy as np

def singleFileRun(fileName):
    file = open(fileName, 'r')
    print(file.read())

def multiFileRun(fileArray):
    if (UIVariables.FileInputs == False):
        return
    fileArray = UIVariables.np.copy()
    index = 0
    while(index < len(fileArray)):
        singleFileRun(fileArray[index])
        index += 1