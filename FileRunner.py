#Program to run a single .yaml file or an array of .yaml files
#to get results for the vectorial model.
#
#Author: Jacob Duffy
#Version: 7/6/2022

import FileCreator
import UIVariables
import astropy.units as u
from astropy.visualization import quantity_support
import pyvectorial as pyv

#Method def for converting between km and astro units
def unitConvert(dataIn):
    return

#Method def for getting the output results for the vectorial model
def singleFileRun(fileName):
    quantity_support()
    #vmc = pyv.vm_configs_from_yaml(fileName)
    #coma = pyv.run_vmodel(vmc)
    #vmr = pyv.get_result_from_coma(coma)
    #pyv.column_density_plots(vmc, vmr, u.km, 1/u.cm**2, True)
    return

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
