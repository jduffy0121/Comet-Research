#Program to create a .yaml file from the results from UIVariables.py.
#Uses a nested dict data type to write the file.
#
#Author: Jacob Duffy
#Version: 7/8/2022

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
    etc = {'print_binned_times' : UIVariables.PrintBinnedTimes, 
    'print_column_density' : UIVariables.PrintColumnDensity, 
    'print_progress' : UIVariables.PrintProgress, 
    'print_radial_density' : UIVariables.PrintRadialDensity,
    'pyv_coma_pickle' : UIVariables.PyvComaPickle,
    'pyv_date_of_run' : datetime.now(),
    'show_3d_column_density_centered' : UIVariables.Show3dColumnDensityCentered,
    'show_3d_column_density_off_center' : UIVariables.Show3dColumnDensityOffCenter,
    'show_agreement_check' : UIVariables.ShowAgreementCheck,
    'show_aperture_checks' : UIVariables.ShowApertureChecks,
    'show_column_density_plots' : UIVariables.ShowColumnDensityPlots,
    'show_fragment_sputter' : UIVariables.ShowFragmentSputter,
    'show_radial_plots' : UIVariables.ShowRadialPlots}

    #Creates the final dictionary and returns it
    VectorialModelConfig = {'production' : production, 'parent' : parent, 'comet' : comet,
    'fragment' : fragment, 'grid' : grid, 'etc' : etc}

    return VectorialModelConfig

#Creates a new .yaml file called data.yaml based on the return val of createDictionary()
def newFile():
    with open(r'pyvectorial.yaml', 'w') as file:
        documents = yaml.dump(createDictionary(), file)

#Deletes a file named fileName
def removeFile(fileName):
    os.remove(fileName)