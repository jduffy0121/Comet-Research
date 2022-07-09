#Program to run a single .yaml file or an array of .yaml files
#to get results for the vectorial model.
#
#Author: Jacob Duffy
#Version: 7/8/2022

import UIVariables
import FileCreator
import yaml
from datetime import datetime
import astropy.units as u
from astropy.visualization import quantity_support
import pyvectorial as pyv

#Method def for converting between km and astro units
def unitConvert(dataIn):
    return

#Method def for getting the output results for the vectorial model
def singleFileRun(fileName):
    quantity_support()
    #vmc = pyv._vm_config_from_yaml(fileName)
    #vmc.etc['print_progress'] = True
    #coma = pyv.run_vmodel(vmc)
    #vmr = pyv.get_result_from_coma(coma)
    #pyv.column_density_plots(vmc, vmr, u.km, 1/u.cm**2, True)
    #pyv.plot_fragment_sputter(vmr.fragment_sputter, dist_units=u.km,
    #                sputter_units=1/u.cm**3, within_r=1000*u.km)

    #OFF CENTERED
    #pyv.column_density_plot_3d(vmc, vmr, x_min=-100000*u.km,
    #                x_max=10000*u.km, y_min=-100000*u.km, y_max=10000*u.km,
    #                grid_step_x=1000, grid_step_y=1000, r_units=u.km,
    #                cd_units=1/u.cm**2)

    #CENTERED
    #pyv.column_density_plot_3d(vmc, vmr, x_min=-100000*u.km,
    #                x_max=100000*u.km, y_min=-100000*u.km, y_max=100000*u.km,
    #                grid_step_x=1000, grid_step_y=1000, r_units=u.km,
    #                cd_units=1/u.cm**2)

    #pyv.radial_density_plots(vmc, vmr, r_units=u.km, voldens_units=1/u.cm**3)
    #return vmr


#Method def for running the program manually (ie: all input is done by user)
def runManualProgram():
    FileCreator.createDictionary()
    FileCreator.newFile()
    singleFileRun(UIVariables.FileName)
    return

#Method def for running the program with file input (yaml)
def runFileYamlProgram():
    singleFileRun(UIVariables.FileName)
    return

def runFilePickleProgram():
    pyv.read_results(UIVariables.FileName)
    return

def pickleTest():
    try:
        pyv.read_results(UIVariables.FileName)
        return True
    except ModuleNotFoundError:
        return False

#Method def for testing a 2 level deep dict value for it being either float/int.
def dictTest2Var(dict, parent, child, type):
    try:
        testing = dict[f'{parent}'][f'{child}']
        if (type == 'float'):
            try:
                float(testing)
                if(float(testing) >= 0):
                    return True
                else:
                    return False
            except ValueError:
                return False
        if (type == 'int'):
            try:
                int(testing)
                if (int(testing) >= 0):
                    return True
                else:
                    return False
            except ValueError:
                return False
        if (type == 'bool'):
            try:
                if((testing) == True or (testing == False)):
                    return True
            except ValueError:
                return False
        if (type == 'none'):
            return True
    except KeyError:
        return False

#Method def for testing all input files with the correct results
def fileTest():
    with open(f"{UIVariables.FileName}", 'r') as file:
        dict = yaml.safe_load(file)
        if(dictTest2Var(dict, 'comet', 'rh', 'float') == False):
            return False
        if(dictTest2Var(dict, 'comet', 'transform_applied', 'bool') == False):
            return False
        if(dictTest2Var(dict, 'fragment', 'v_photo', 'float') == False):
            return False
        if(dictTest2Var(dict, 'grid', 'angular_points', 'int') == False):
            return False
        if(dictTest2Var(dict, 'grid', 'radial_points', 'int') == False):
            return False
        if(dictTest2Var(dict, 'grid', 'radial_substeps', 'int') == False):
            return False
        if(dictTest2Var(dict, 'parent', 'T_to_d_ratio', 'float') == False):
            return False
        if(dictTest2Var(dict, 'parent', 'sigma', 'float') == False):
            return False
        if(dictTest2Var(dict, 'parent', 'tau_T', 'float') == False):
            return False
        if(dictTest2Var(dict, 'parent', 'tau_d', 'float') == False):
           return False
        if(dictTest2Var(dict, 'parent', 'v_outflow', 'float') == False):
            return False
        if(dictTest2Var(dict, 'production', 'base_q', 'float') == False):
            return False
        dict['etc'] = {}
        dict['etc']['print_binned_times'] = UIVariables.PrintBinnedTimes
        dict['etc']['print_column_density'] = UIVariables.PrintColumnDensity
        dict['etc']['print_progress'] = UIVariables.PrintProgress
        dict['etc']['print_radial_density'] = UIVariables.PrintRadialDensity
        dict['etc']['pyv_coma_pickle'] = UIVariables.PyvComaPickle
        dict['etc']['pyv_date_of_run'] = datetime.now()
        dict['etc']['show_3d_column_density_centered'] = UIVariables.Show3dColumnDensityCentered
        dict['etc']['show_3d_column_density_off_center'] = UIVariables.Show3dColumnDensityOffCenter
        dict['etc']['show_agreement_check'] = UIVariables.ShowAgreementCheck
        dict['etc']['show_aperture_checks'] = UIVariables.ShowApertureChecks
        dict['etc']['show_column_density_plots'] = UIVariables.ShowColumnDensityPlots
        dict['etc']['show_fragment_sputter'] = UIVariables.ShowFragmentSputter
        dict['etc']['show_radial_plots'] = UIVariables.ShowRadialPlots
        with open(f'{UIVariables.FileName}', 'w') as newerFile:
            documents = yaml.dump(dict, newerFile)
            newerFile.close()
        file.close()
    return True
