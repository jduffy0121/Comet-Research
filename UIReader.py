#Program to read the UI interface from UICreator.py for direct user 
#inputs and returns the correct data type.
#Raises exceptions from UIExceptions.py if the user's data can not be converted 
#to the correct data type.
#Information is referenced in FileCreator.py.
#
#Author: Jacob Duffy
#Version: 6/28/2022

import UICreator
import UIExceptions
from datetime import datetime

#Return methods for production.
class production():
    def getBaseQ():
        return 1e28
    def getTimeVariationType():
        return 'TimeVarTypes'
    def getAmplitude():
        return 10
    def getParamDelta():
        return 11
    def getPeriod():
        return 12

#Return methods for parent.
class parent():
    def getName():
        return 'ParentName'
    def getVOutflow():
        return 100
    def getTauD():
        return 101
    def getTauT():
        return 102
    def getSigma():
        return 103
    def getTtoDRatio():
        return 104

#Return methods for fragment.
class fragment():
    def getName():
        return 'FragName'
    def getVPhoto():
        return 105
    def getTauT():
        return 106

#Return methods for comet.
class comet():
    def getName():
        return 'CometName'
    def getRH():
        return 107
    def getDelta():
        return 108
    def getTransformMethod():
        return 'TransformMethod'
    def getTransformApplied():
        return True

#Return methods for grid.
class grid():
    def getAngularPoints():
        return 20
    def getRadialPoints():
        return 21
    def getRadialSubsteps():
        return 22

#Return mehtods for etc.
class etc():
    def getPrintBinnedTimes():
        return False
    def getPrintColumnDensity():
        return True
    def getPrintProgress():
        return False
    def getPrintRadialDensity():
        return True
    def getPyvComaPickle():
        return 'ComaPickle'
    def getPyvDateOfRun():
        return datetime.now()
    def getShow3dColumnDensityCentered(): 
        return True
    def getShow3dColumnDensityOffCenter():
        return False
    def getShowAgreementCheck():
        return True
    def getShowApertureChecks():
        return False
    def getShowColumnDensityPlots():
        return True
    def getShowFragmentSputter():
        return False
    def getShowRadialPlots():
        return True