#Program to create a .yaml file from the results from UIReader.py.
#Uses a nested dict data type to write the file.
#
#Author: Jacob Duffy
#Version: 6/29/2022

import yaml
import UIVariables
from datetime import datetime

def createDictory():
    params = {'amplitude' : UIVariables.Amplitude, 
    'delta' : UIVariables.ParamDelta,
    'period' : UIVariables.Period}

    production = {'base_q' : UIVariables.BaseQ,
    'time_variation_type' : UIVariables.TimeVariationType, 'params' : params}

    parent = {'name' : UIVariables.ParentName, 
    'v_outflow' : UIVariables.VOutflow, 
    'tau_d' : UIVariables.TauD, 'tau_T' : UIVariables.TauTParent, 
    'sigma' : UIVariables.Sigma, 'T_to_d_ratio' : UIVariables.TtoDRatio}

    fragment = {'name' : UIVariables.FragmentName, 
    'v_photo' : UIVariables.VPhoto, 
    'tau_T' : UIVariables.TauTParent}

    comet = {'name' : UIVariables.CometName, 'rh' : UIVariables.RH, 
    'delta' : UIVariables.CometDelta, 
    'transform_method' : UIVariables.TransformMethod, 
    'transform_applied' : UIVariables.ApplyTransforMethod}

    grid = {'radial_points' : UIVariables.RadialPoints, 
    'angular_points' : UIVariables.AngularPoints, 
    'radial_substeps' : UIVariables.RadialSubsteps}

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

    VectorialModelConfig = {'production' : production, 'parent' : parent, 'comet' : comet,
    'fragment' : fragment, 'grid' : grid, 'etc' : etc}

    return VectorialModelConfig

def newFile():
    with open(r'test.yaml', 'w') as file:
        documents = yaml.dump(createDictory(), file)