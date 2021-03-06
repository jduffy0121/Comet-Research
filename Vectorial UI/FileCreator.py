#Program to create a .yaml file from the results from UIVariables.py.
#Uses a nested dict data type to write the file.
#
#Author: Jacob Duffy
#Version: 7/16/2022

import UIVariables
import yaml
import os
from datetime import datetime

#Method to create a dictionary based on the variables in UIVariables.py
#Returns the completed dictionary
def createDictionary():

    #Creates the production dictionary
    if(UIVariables.TimeVariationType == 'sine wave'):
        params = {'amplitude' : UIVariables.SinAmp, 'period' : UIVariables.SinPer,
        'delta' : UIVariables.SinDelta}
        production = {'base_q' : UIVariables.BaseQ,
        'time_variation_type' : UIVariables.TimeVariationType, 'params' : params}
    elif(UIVariables.TimeVariationType == 'gaussian'):
        params = {'amplitude' : UIVariables.GausAmp, 'std_dev' : UIVariables.GausSTD,
        't_max' : UIVariables.GausT_Max}
        production = {'base_q' : UIVariables.BaseQ,
        'time_variation_type' : UIVariables.TimeVariationType, 'params' : params}
    elif(UIVariables.TimeVariationType == 'square pulse'):
        params = {'amplitude' : UIVariables.SquareAmp, 'duration' : UIVariables.SquareDur,
        't_start' : UIVariables.SquareT_Start}
        production = {'base_q' : UIVariables.BaseQ,
        'time_variation_type' : UIVariables.TimeVariationType, 'params' : params}
    else:
        production = {'base_q' : UIVariables.BaseQ,
        'time_variation_type' : UIVariables.TimeVariationType}   

    #Creates the parent dictionary
    parent = {'name' : UIVariables.ParentName, 
    'v_outflow' : UIVariables.VOutflow, 
    'tau_d' : UIVariables.TauD, 'tau_T' : UIVariables.TauTParent, 
    'sigma' : UIVariables.Sigma, 'T_to_d_ratio' : UIVariables.TtoDRatio}

    #Creates the fragment dictionary
    fragment = {'name' : UIVariables.FragmentName, 
    'v_photo' : UIVariables.VPhoto, 
    'tau_T' : UIVariables.TauTParent}

    #Creates the comet dictionary
    comet = {'name' : UIVariables.CometName, 'rh' : UIVariables.Rh, 
    'delta' : UIVariables.CometDelta, 
    'transform_method' : UIVariables.TransformMethod, 
    'transform_applied' : UIVariables.ApplyTransforMethod}

    #Creates the grid dictionary
    grid = {'radial_points' : UIVariables.RadialPoints, 
    'angular_points' : UIVariables.AngularPoints, 
    'radial_substeps' : UIVariables.RadialSubsteps}

    #Creates the etc dictionary
    etc = {'print_binned_times' : True, 'print_column_density' : True, 
    'print_progress' : True, 'print_radial_density' : True,
    'pyv_coma_pickle' : UIVariables.PyvComaPickle,
    'pyv_date_of_run' : datetime.now(), 'show_3d_column_density_centered' : True,
    'show_3d_column_density_off_center' : True, 'show_agreement_check' : True,
    'show_aperture_checks' : True, 'show_column_density_plots' : True,
    'show_fragment_sputter' : True, 'show_radial_plots' : True}

    #Creates the final dictionary and returns it
    dict = {'production' : production, 'parent' : parent, 'comet' : comet,
    'fragment' : fragment, 'grid' : grid, 'etc' : etc}

    return dict

#Creates a new .yaml file called pyvectorial.yaml based on the return val of createDictionary()
def newFileManual():
    with open(r'pyvectorial.yaml', 'w') as file:
        documents = yaml.dump(createDictionary(), file)

#Creates a new .yaml file saved to a filePath (including file name) with a given dict imput
def newFileInputs(filePath, dict):
    with open(f'{filePath}', 'w') as file:
        documents = yaml.dump(dict, file)

#Deletes a file named fileName
def removeFile(fileName):
    os.remove(fileName)