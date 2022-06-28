#Program to create a .yaml file from the results from UIReader.py.
#Uses a nested dict data type to write the file.
#
#Author: Jacob Duffy
#Version: 6/28/2022

import yaml
import UIReader

def createDictory():
    params = {'amplitude' : UIReader.production.getAmplitude(), 
    'delta' : UIReader.production.getParamDelta(),
    'period' : UIReader.production.getPeriod()}

    production = {'base_q' : UIReader.production.getBaseQ(), 
    'time_variation_type' : UIReader.production.getTimeVariationType(), 'params' : params}

    parent = {'name' : UIReader.parent.getName(), 
    'v_outflow' : UIReader.parent.getVOutflow(), 
    'tau_d' : UIReader.parent.getTauD(), 'tau_T' : UIReader.parent.getTauT(), 
    'sigma' : UIReader.parent.getSigma(), 'T_to_d_ratio' : UIReader.parent.getTtoDRatio()}

    fragment = {'name' : UIReader.fragment.getName(), 
    'v_photo' : UIReader.fragment.getVPhoto(), 
    'tau_T' : UIReader.fragment.getTauT()}

    comet = {'name' : UIReader.comet.getName(), 'rh' : UIReader.comet.getRH(), 
    'delta' : UIReader.comet.getDelta(), 
    'transform_method' : UIReader.comet.getTransformMethod(), 
    'transform_applied' : UIReader.comet.getTransformApplied()}

    grid = {'radial_points' : UIReader.grid.getRadialPoints(), 
    'angular_points' : UIReader.grid.getAngularPoints(), 
    'radial_substeps' : UIReader.grid.getRadialSubsteps()}

    etc = {'print_binned_times' : UIReader.etc.getPrintBinnedTimes(), 
    'print_column_density' : UIReader.etc.getPrintColumnDensity(), 
    'print_progress' : UIReader.etc.getPrintProgress(), 
    'print_radial_density' : UIReader.etc.getPrintRadialDensity(),
    'pyv_coma_pickle' : UIReader.etc.getPyvComaPickle(),
    'pyv_date_of_run' : UIReader.etc.getPyvDateOfRun(),
    'show_3d_column_density_centered' : UIReader.etc.getShow3dColumnDensityCentered(),
    'show_3d_column_density_off_center' : UIReader.etc.getShow3dColumnDensityOffCenter(),
    'show_agreement_check' : UIReader.etc.getShowAgreementCheck(),
    'show_aperture_checks' : UIReader.etc.getShowApertureChecks(),
    'show_column_density_plots' : UIReader.etc.getShowColumnDensityPlots(),
    'show_fragment_sputter' : UIReader.etc.getShowFragmentSputter(),
    'show_radial_plots' : UIReader.etc.getShowRadialPlots()}

    VectorialModelConfig = {'production' : production, 'parent' : parent, 'comet' : comet,
    'fragment' : fragment, 'grid' : grid, 'etc' : etc}

    return VectorialModelConfig

with open(r'test.yaml', 'w') as file:
    documents = yaml.dump(createDictory(), file)