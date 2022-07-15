#Program to run a single .yaml file or pickle file to get results for the vectorial model.
#Sends the created vmc and vmr to UICreator.py to display the results.
#This is the only program related to the UI that references pyvectorial directly.
#
#Author: Jacob Duffy
#Version: 7/15/2022

import UIVariables
import FileCreator
import pyvectorial as pyv
import yaml
import io
import astropy.units as u
from datetime import datetime
from astropy.visualization import quantity_support
from contextlib import redirect_stdout

#Method def for getting the output results for the vectorial model
def singleFileRun(fileName):
    quantity_support()
    vmc = pyv._vm_config_from_yaml(fileName) #Creates the vmc object
    coma = pyv.run_vmodel(vmc) #Creates the coma object
    vmr = pyv.get_result_from_coma(coma) #Creates the vmr object
    with io.StringIO() as buf, redirect_stdout(buf): #Gets all the print() from show_aperture_checks() and saves it to UIVariables
        pyv.show_aperture_checks(coma)
        UIVariables.ApertureChecks = buf.getvalue()
    return vmc, vmr


#Method def for running the program manually (ie: all input is done by user)
def runManualProgram():
    FileCreator.createDictionary() #Creates a new dict for the user inputs
    FileCreator.newFile() #Creates a new yaml file
    return singleFileRun(UIVariables.FileName) #Runs the program, returning a vmc and vmr
    

#Method def for running the program with file input (yaml)
def runFileYamlProgram():
    return singleFileRun(UIVariables.FileName)
    

#Method def for running the program with file input (pickle)
def runFilePickleProgram():
    vmc = pyv.VectorialModelConfig(production=None, parent=None, fragment=pyv.Fragment(name ='unknown', v_photo=None, tau_T=None), comet=None, grid=None, etc=None) #Creates a default vmc
    vmr = pyv.read_results(UIVariables.FileName) #Creates a vmr from the pickle
    return vmc, vmr

#Method def for testing if the program can read a given pickle file
def pickleTest():
    try:
        pyv.read_results(UIVariables.FileName)
        return True
    except ModuleNotFoundError:
        return False

#Method def for testing if a data value is a float or int and if val >= 0 or if a val is a bool
def valueTest(input, type):
    if (type == 'float'): #Test if val is a float
        try:
            val = float(input)
            if (val >= 0):
                return True
            else:
                return False
        except ValueError:
            return False
    if (type == 'int'): #Test if val is an int
        try:
            val = int(input)
            if (val >= 0):
                return True
            else:
                return False
        except ValueError:
            return False
    if (type == 'bool'): #Test if val is a bool
        try:
            val = bool(input)
            return True
        except ValueError:
            return False

#Method def for testing a 2 level deep dict value for it being either float/int/bool
def dictTest(dict, parent, child, type, grandchild=None):
    try:
        if(grandchild == None): #Creates a "2 deep level" dict test 
            testing = dict[f'{parent}'][f'{child}']
        else: #Creates a "3 deep level" dict test
            testing = dict[f'{parent}'][f'{child}'][f'{grandchild}']
        if (type == 'float' and valueTest(testing, 'float')): #Test if the dict value is a float
            return True
        elif (type == 'int' and valueTest(testing, 'int')): #Test if the dict value is an int
            return True
        elif (type == 'bool' and valueTest(testing, 'bool')): #Test if the dict value is a bool
            return True
        elif(type == 'any'): #Test if the dict value exist, regardless of its data type
            return True
        else:
            return False
    except KeyError:
        return False

#Method def for testing all input files with the correct results
def fileTest():
    with open(f"{UIVariables.FileName}", 'r') as file: #Opens the user yaml file
        dict = yaml.safe_load(file)
        if(dictTest(dict, 'comet', 'rh', 'float') == False): #Test and sees if the dict value is a correct data type
            return False
        if(dictTest(dict, 'comet', 'transform_method', 'any') == False):
            return False
        if((dict['comet']['transform_method'] != 'cochran_schleicher_93') and #Sees if the transform_method is assigned properly
            (dict['comet']['transform_method'] != 'festou_fortran') and
            (dict['comet']['transform_method'] != None)):
            return False
        if(dictTest(dict, 'comet', 'transform_applied', 'bool') == False):
            return False
        if(dictTest(dict, 'fragment', 'v_photo', 'float') == False):
            return False
        if(dictTest(dict, 'grid', 'angular_points', 'int') == False):
            return False
        if(dictTest(dict, 'grid', 'radial_points', 'int') == False):
            return False
        if(dictTest(dict, 'grid', 'radial_substeps', 'int') == False):
            return False
        if(dictTest(dict, 'parent', 'T_to_d_ratio', 'float') == False):
            return False
        if(dictTest(dict, 'parent', 'sigma', 'float') == False):
            return False
        if(dictTest(dict, 'parent', 'tau_d', 'float') == False):
           return False
        if(dictTest(dict, 'parent', 'v_outflow', 'float') == False):
            return False
        if(dictTest(dict, 'production', 'base_q', 'float') == False):
            return False
        if(dictTest(dict, 'production', 'time_variation_type', 'any') == False): #Sees if dict['production']['time_variation_type'] is real
            return False
        if(dict['production']['time_variation_type'] == 'sine wave'): #Sees if the time variation is a sine and checks all the params
            if(dictTest(dict, 'production', 'params', 'float', 'amplitude') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 'delta') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 'period') == False):
                return False
        elif(dict['production']['time_variation_type'] == 'gaussian'): #Sees if the time variation is a gaussian and checks all the params
            if(dictTest(dict, 'production', 'params', 'float', 'amplitude') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 'std_dev') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 't_max') == False):
                return False
        elif(dict['production']['time_variation_type'] == 'square pulse'): #Sees if the time variation is a square and checks all the params
            if(dictTest(dict, 'production', 'params', 'float', 'amplitude') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 'duration') == False):
                return False
            if(dictTest(dict, 'production', 'params', 'float', 't_start') == False):
                return False
        elif(dict['production']['time_variation_type'] != None): #Sees if the time variation is not null, which means it is a different string/object then what is allowed for pyvectorial
            return False
        dict['etc'] = {} #Creates the etc section for the dict
        dict['etc']['print_binned_times'] = True
        dict['etc']['print_column_density'] = True
        dict['etc']['print_progress'] = True
        dict['etc']['print_radial_density'] = True
        dict['etc']['pyv_coma_pickle'] = UIVariables.PyvComaPickle
        dict['etc']['pyv_date_of_run'] = datetime.now()
        dict['etc']['show_3d_column_density_centered'] = True
        dict['etc']['show_3d_column_density_off_center'] = True
        dict['etc']['show_agreement_check'] = True
        dict['etc']['show_aperture_checks'] = True
        dict['etc']['show_column_density_plots'] = True
        dict['etc']['show_fragment_sputter'] = True
        dict['etc']['show_radial_plots'] = True
        with open(f'{UIVariables.FileName}', 'w') as newerFile: #Opens a new file
            documents = yaml.dump(dict, newerFile) #Creates a new yaml file with the new etc section, replacing the old one
            newerFile.close()
        file.close()
    return True

#Gets the radial plot from pyvectorial
#Returns the figure
def getRadialPlots(vmc, vmr):
    return pyv.radial_density_plots(vmc, vmr, r_units=u.km, voldens_units=1/u.cm**3, show_plots=False)[1]

#Gets the fragment sputter plot from pyvectorial
#Returns the figure
def getFragSputter(vmc, vmr):
    return pyv.plot_fragment_sputter(vmr.fragment_sputter, dist_units=u.km, sputter_units=1/u.cm**3, within_r=1000*u.km, show_plots=False)[1]

#Gets the column density from pyvectorial
#Returns the figure
def getColumnDensity(vmc, vmr):
    return pyv.column_density_plots(vmc, vmr, u.km, 1/u.cm**2, show_plots=False)[1]

#Gets the 3d column density plot from pyvectorial
#Returns the figure
def get3DColumnDensity(vmc, vmr):
    return pyv.column_density_plot_3d(vmc, vmr, x_min=-100000*u.km,
                   x_max=10000*u.km, y_min=-100000*u.km, y_max=10000*u.km,
                    grid_step_x=1000, grid_step_y=1000, r_units=u.km,
                    cd_units=1/u.cm**2, show_plots=False)[1]

#Gets the 3d colum density plot centered from pyvectorial
#Returns the figure
def get3DColumnDensityCentered(vmc, vmr):
    return pyv.column_density_plot_3d(vmc, vmr, x_min=-100000*u.km,
                   x_max=100000*u.km, y_min=-100000*u.km, y_max=100000*u.km,
                   grid_step_x=1000, grid_step_y=1000, r_units=u.km,
                   cd_units=1/u.cm**2, show_plots=False)[1]

#Gets the radial density from a given vmr
def getPrintRadialDensity(vmr):
    with io.StringIO() as buf, redirect_stdout(buf):
        pyv.print_radial_density(vmr)
        result = buf.getvalue()
    return result
    
#Gets the column density from a given vmr
def getPrintColumnDensity(vmr):
    with io.StringIO() as buf, redirect_stdout(buf):
        pyv.print_column_density(vmr)
        result = buf.getvalue()
    return result

#Gets the agreement check from a given vmr
def getAgreementCheck(vmr):
    with io.StringIO() as buf, redirect_stdout(buf):
        pyv.show_fragment_agreement(vmr)
        result = buf.getvalue()
    return result
