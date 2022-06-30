#Program that contains global variables used in the UI.
#
#Author: Jacob Duffy
#Version: 6/30/2022

FileArray = []
DownloadFilePath = None
ManInputs = False
FileInputs = False
KeepFile = False

#Production variables
BaseQ = None
TimeVariationType = None
Amplitude = None
ParamDelta = None
Period = None

#Parent variables
ParentName = None
VOutflow = None
TauD = None
TauTParent = None
Sigma = None
TtoDRatio = None

#Fragment variables
FragmentName = None
VPhoto = None
TauTFragment = None

#Comet variables
CometName = None
Rh = None
CometDelta = None
TransformMethod = None
ApplyTransforMethod = False

#Grid variables
AngularPoints = None
RadialPoints = None
RadialSubsteps = None

#Etc variables
PrintBinnedTimes = False
PrintColumnDensity = False
PrintProgress = False
PrintRadialDensity = False
PyvComaPickle = False
PyvDateOfRun = None
Show3dColumnDensityCentered = False
Show3dColumnDensityOffCenter = False
ShowAgreementCheck = False
ShowApertureChecks = False
ShowColumnDensityPlots = False
ShowFragmentSputter = False
ShowRadialPlots = False