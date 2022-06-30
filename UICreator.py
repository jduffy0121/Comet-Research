#Driver program to create a UI to read in vectorial model data for comet analysis.
#Uses PyQt5 as the interface to create the UI.
#This work is based on a pvvectorial repository created by sjoset.
#
#Author: Jacob Duffy
#Version: 6/29/2022

import UIVariables
import FileCreator
import FileRunner
import sys
import os.path
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QCheckBox, QVBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QScrollBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot

#Method def for running the program manually (ie: all input is done by user)
def runManualProgram():
    FileCreator.createDictionary()
    FileCreator.newFile()
    FileRunner.singleFileRun('data.yaml')
    #FileCreator.removeFile('data.yaml')

#Method def for running the program with file inputs
def runFileProgram():
    return None

#Class to give a new pop up window to the user more info about proper usage of the Main UI.
class MoreWindow(QWidget):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'More Information'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.text = QLabel("More info", self)
        self.text.move(500,500)
        self.show()

#Main UI Window, Driver Class. 
#Used to create/format the UI, read/test in all user data into UIVariables.py,
#reference other child UI windows, run the program and create a new window with the results
class App(QMainWindow):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'Vectorial Model Input UI'
        self.left = 10
        self.top = 10
        self.width = 2200
        self.height = 1400
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Creates title headers for the UI
        self.box1 = QLabel("Manual Inputs", self)
        self.box1.move(570,10)
        self.box1.setFont((QFont('Arial', 18)))
        self.box1.resize(550,60)
        self.box2 = QLabel("File Inputs", self)
        self.box2.move(900,950)
        self.box2.setFont((QFont('Arial', 18)))
        self.box2.resize(550,60)
        self.box3 = QLabel("Extra Options", self)
        self.box3.move(1650,10)
        self.box3.setFont((QFont('Arial', 18)))
        self.box3.resize(550,60)
        self.box4 = QLabel("File Downloads", self)
        self.box4.move(1650,950)
        self.box4.setFont((QFont('Arial', 18)))
        self.box4.resize(550,60)
        
        ##Creates manual input UI elements for the Production section
        self.textPro = QLabel("Production Variables", self)
        self.textPro.setFont((QFont('Arial', 12)))
        self.textPro.move(50,160)
        self.textPro.resize(400,40)
        BaseQText = QLabel("Input Base Q: ", self)
        BaseQText.move(20,220)
        BaseQText.resize(180,40)
        self.BaseQBox = QLineEdit(self)
        self.BaseQBox.move(200,220)
        self.BaseQBox.resize(180,40)
        BaseQUnits = QLabel("prod/sec", self)
        BaseQUnits.move(400,220)
        BaseQUnits.resize(180,40)
        TimeTVText = QLabel("*Input Time Variation Type: ", self)
        TimeTVText.move(20,280)
        TimeTVText.resize(400,40)
        self.TimeTVBox = QLineEdit(self)
        self.TimeTVBox.move(360,280)
        self.TimeTVBox.resize(180,40)
        AmpText = QLabel("Input Amplitude: ", self)
        AmpText.move(20,340)
        AmpText.resize(400,40)
        self.AmpBox = QLineEdit(self)
        self.AmpBox.move(240,340)
        self.AmpBox.resize(180,40)
        ParamDeltaText = QLabel("Input Delta: ", self)
        ParamDeltaText.move(20,400)
        ParamDeltaText.resize(400,40)
        self.ParamDeltaBox = QLineEdit(self)
        self.ParamDeltaBox.move(180,400)
        self.ParamDeltaBox.resize(180,40)
        PeriodText = QLabel("Input Period: ", self)
        PeriodText.move(20,460)
        PeriodText.resize(400,40)
        self.PeriodBox = QLineEdit(self)
        self.PeriodBox.move(190,460)
        self.PeriodBox.resize(180,40)

        ##Creates manual input UI elements for the Parent section
        self.textPar = QLabel("Parent Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(50,560)
        self.textPar.resize(400,40)
        ParNameText = QLabel("Input Parent Name: ", self)
        ParNameText.move(20,620)
        ParNameText.resize(300,40)
        self.ParNameBox = QLineEdit(self)
        self.ParNameBox.move(260,620)
        self.ParNameBox.resize(180,40)
        OutVText = QLabel("Input Outflow Velocity: ", self)
        OutVText.move(20,680)
        OutVText.resize(300,40)
        self.OutVBox = QLineEdit(self)
        self.OutVBox.move(300,680)
        self.OutVBox.resize(180,40)
        TauDText = QLabel("Input Tau_D: ", self)
        TauDText.move(20,740)
        TauDText.resize(300,40)
        self.TauDBox = QLineEdit(self)
        self.TauDBox.move(185,740)
        self.TauDBox.resize(180,40)
        TauTParText = QLabel("Input Tau_T: ", self)
        TauTParText.move(20,800)
        TauTParText.resize(300,40)
        self.TauTParBox = QLineEdit(self)
        self.TauTParBox.move(185,800)
        self.TauTParBox.resize(180,40)
        SigmaText = QLabel("Input Sigma: ", self)
        SigmaText.move(20,860)
        SigmaText.resize(300,40)
        self.SigmaBox = QLineEdit(self)
        self.SigmaBox.move(185,860)
        self.SigmaBox.resize(180,40)
        T_DText = QLabel("Input T to D Ratio: ", self)
        T_DText.move(20,920)
        T_DText.resize(300,40)
        self.T_DBox = QLineEdit(self)
        self.T_DBox.move(250,920)
        self.T_DBox.resize(180,40) 

        ##Creates manual input UI elements for the Fragment section  
        self.textFrag = QLabel("Fragment Variables", self)
        self.textFrag.setFont((QFont('Arial', 12)))
        self.textFrag.move(50,1020)
        self.textFrag.resize(400,40) 
        FragNameText = QLabel("Input Fragment Name: ", self)
        FragNameText.move(20,1080)
        FragNameText.resize(300,40)
        self.FragNameBox = QLineEdit(self)
        self.FragNameBox.move(300,1080)
        self.FragNameBox.resize(180,40)  
        VPhotoText = QLabel("Input VPhoto: ", self)
        VPhotoText.move(20,1140)
        VPhotoText.resize(300,40)
        self.VPhotoBox = QLineEdit(self)
        self.VPhotoBox.move(190,1140)
        self.VPhotoBox.resize(180,40)
        TauTFragText = QLabel("Input Tau_T: ", self)
        TauTFragText.move(20,1200)
        TauTFragText.resize(300,40)
        self.TauTFragBox = QLineEdit(self)
        self.TauTFragBox.move(185,1200)
        self.TauTFragBox.resize(180,40)    

        ##Creates manual input UI elements for the Comet section
        self.textPar = QLabel("Comet Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(880,160)
        self.textPar.resize(400,40)
        CometNameText = QLabel("Input Comet Name: ", self)
        CometNameText.move(850,220)
        CometNameText.resize(300,40)
        self.CometNameBox = QLineEdit(self)
        self.CometNameBox.move(1100,220)
        self.CometNameBox.resize(180,40) 
        RHText = QLabel("Input RH: ", self)
        RHText.move(850,280)
        RHText.resize(300,40)
        self.RHBox = QLineEdit(self)
        self.RHBox.move(980,280)
        self.RHBox.resize(180,40)
        DeltaComText = QLabel("Input Delta: ", self)
        DeltaComText.move(850,340)
        DeltaComText.resize(300,40)
        self.DeltaComBox = QLineEdit(self)
        self.DeltaComBox.move(1000,340)
        self.DeltaComBox.resize(180,40)
        TFMethText = QLabel("*Input Transformation Method: ", self)
        TFMethText.move(850,400)
        TFMethText.resize(450,40)
        self.TFMethBox = QLineEdit(self)
        self.TFMethBox.move(1230,400)
        self.TFMethBox.resize(180,40)
        self.TFApplied = QCheckBox("Apply Transformation Method", self)
        self.TFApplied.setChecked(False)
        self.TFApplied.move(850,460)
        self.TFApplied.resize(500,40)

        #Creates manual input UI elements for the Grid section
        self.textGrid = QLabel("Grid Variables", self)
        self.textGrid.setFont((QFont('Arial', 12)))
        self.textGrid.move(880,560)
        self.textGrid.resize(400,40)
        APointsText = QLabel("Input Angular Points: ", self)
        APointsText.move(850,620)
        APointsText.resize(450,40)
        self.APointsBox = QLineEdit(self)
        self.APointsBox.move(1115,620)
        self.APointsBox.resize(180,40)
        RadPointsText = QLabel("Input Radial Points: ", self)
        RadPointsText.move(850,680)
        RadPointsText.resize(450,40)
        self.RadPointsBox = QLineEdit(self)
        self.RadPointsBox.move(1110,680)
        self.RadPointsBox.resize(180,40)
        RadSubText = QLabel("Input Radial Substeps: ", self)
        RadSubText.move(850,740)
        RadSubText.resize(450,40)
        self.RadSubBox = QLineEdit(self)
        self.RadSubBox.move(1130,740)
        self.RadSubBox.resize(180,40)

        #Creates UI elements for the extra check boxes that can be used by both input types
        self.BinTimesBox = QCheckBox("Print Binned Times", self)
        self.BinTimesBox.setChecked(False)
        self.BinTimesBox.move(1610,110)
        self.BinTimesBox.resize(500,40)
        self.ColumDBox = QCheckBox("Print Column Density", self)
        self.ColumDBox.setChecked(False)
        self.ColumDBox.move(1610,170)
        self.ColumDBox.resize(500,40)
        self.PrintPBox = QCheckBox("Print Progress", self)
        self.PrintPBox.setChecked(False)
        self.PrintPBox.move(1610,230)
        self.PrintPBox.resize(500,40)
        self.PrintRadDBox = QCheckBox("Print Radial Density", self)
        self.PrintRadDBox.setChecked(False)
        self.PrintRadDBox.move(1610,290)
        self.PrintRadDBox.resize(500,40)
        self.PickleBox = QCheckBox("*Pyv Coma Pickle", self)
        self.PickleBox.setChecked(False)
        self.PickleBox.move(1610,350)
        self.PickleBox.resize(500,40)
        self.DCenterBox = QCheckBox("Show 3D Column Density Centered", self)
        self.DCenterBox.setChecked(False)
        self.DCenterBox.move(1610,410)
        self.DCenterBox.resize(500,40)
        self.DNotCenterBox = QCheckBox("Show 3D Column Density Off Centered", self)
        self.DNotCenterBox.setChecked(False)
        self.DNotCenterBox.move(1610,470)
        self.DNotCenterBox.resize(550,40)
        self.AgreeCheck = QCheckBox("Show Agreement Checks", self)
        self.AgreeCheck.setChecked(False)
        self.AgreeCheck.move(1610,530)
        self.AgreeCheck.resize(500,40)
        self.ApeCheck = QCheckBox("Show Aperture Checks", self)
        self.ApeCheck.setChecked(False)
        self.ApeCheck.move(1610,590)
        self.ApeCheck.resize(500,40)
        self.ColumPlotBox = QCheckBox("Show Column Density Plots", self)
        self.ColumPlotBox.setChecked(False)
        self.ColumPlotBox.move(1610,650)
        self.ColumPlotBox.resize(550,40)
        self.FragSputBox = QCheckBox("Show Fragment Sputter", self)
        self.FragSputBox.setChecked(False)
        self.FragSputBox.move(1610,710)
        self.FragSputBox.resize(500,40)
        self.RadPlotBox = QCheckBox("Show Radial Plots", self)
        self.RadPlotBox.setChecked(False)
        self.RadPlotBox.move(1610,770)
        self.RadPlotBox.resize(500,40)

        #Creates other UI elements such as certain check boxes/text UI stuff
        self.FileInputBox = QCheckBox("*Select for File Inputs", self)
        self.FileInputBox.setChecked(False)
        self.FileInputBox.move(870,1040)
        self.FileInputBox.resize(500,40)
        self.ManInputBox = QCheckBox("Select for Manual Inputs", self)
        self.ManInputBox.setChecked(False)
        self.ManInputBox.move(540,100)
        self.ManInputBox.resize(500,40)
        self.DownInputBox = QCheckBox("Select for File Downloads", self)
        self.DownInputBox.setChecked(False)
        self.DownInputBox.move(1620,1040)
        self.DownInputBox.resize(500,40)
        DownText = QLabel("Input File Path for Downloads", self)
        DownText.move(1620,1100)
        DownText.resize(500,40)
        self.DownTextBox = QLineEdit(self)
        self.DownTextBox.move(1620,1160)
        self.DownTextBox.resize(400,40)
        self.button = QPushButton('Run Program', self)
        self.button.move(1700,1320)
        self.button.resize(400,40)
        self.button.clicked.connect(self.runProg)
        self.file = QPushButton('File Upload', self)
        self.file.move(870,1100)
        self.file.resize(400,40)
        self.file.clicked.connect(self.fileInp)
        self.more = QPushButton('*More Information', self)
        self.more.move(20,1320)
        self.more.resize(400,40)
        self.more.clicked.connect(self.moreInfo)
        self.fileOut = QListWidget(self)
        self.fileOut.setGeometry(200, 400, 400, 200)
        self.fileOut.move(870,1160)
        self.scrollBar = QScrollBar(self)
        self.fileOut.setVerticalScrollBar(self.scrollBar)

        #Creates the UI
        self.show()

    #Error Throws
    #No input type is selected by the user (either manual or file)
    def noInput(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("No input type selected.")
        self.message.show()
    
    #Missing a critical text box entry
    def emptyBox(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("Missing text box entry.")
        self.message.show()
    
    #Gave an incorrect data type for the manual data entry (almost always string could not
    #be converted to a float/int)
    def incorrectDataType(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("Incorrect manual data entry, check each input to make sure it has been entered properly.")
        self.message.show()

    #Gave an incorrect path for where the user wished to store the results of the program
    def noPathFound(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("No download path found, unable to download files.")
        self.message.show()
    
    #Program ran successfully, there should not be any errors
    def successRun(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)
        self.message.setWindowTitle("Success")
        self.message.setText("Program run successful!")
        self.message.show()
    
    #Run Program
    def runProg(self):

        #Sees if the user selected to have downloads and checks to confirm the path is correct.
        if(self.DownInputBox.isChecked() == True):
            if (os.path.isdir(self.DownTextBox.text()) == True):
                UIVariables.DownloadFilePath = self.DownTextBox.text()
            else:
                self.noPathFound()
                return

        #Manual input runner
        #Test proper user input and assigns the proper results to global variables in UIVariables.py
        if(self.ManInputBox.isChecked() == True):
            UIVariables.ManInputs = True

            #Param Declarations
            UIVariables.BaseQ = self.BaseQBox.text()
            UIVariables.TimeVariationType = self.TimeTVBox.text()
            UIVariables.Amplitude = self.AmpBox.text()
            UIVariables.ParamDelta = self.ParamDeltaBox.text()
            UIVariables.Period = self.PeriodBox.text()

            #Parent Declarations
            UIVariables.ParentName = self.ParNameBox.text()
            UIVariables.VOutflow = self.OutVBox.text()
            UIVariables.TauD = self.TauDBox.text()
            UIVariables.TauTParent = self.TauTParBox.text()
            UIVariables.Sigma = self.SigmaBox.text()
            UIVariables.TtoDRatio = self.T_DBox.text()

            #Fragment Declarations
            UIVariables.FragmentName = self.FragNameBox.text()
            UIVariables.VPhoto = self.VPhotoBox.text()
            UIVariables.TauTFragment = self.TauTFragBox.text()

            #Comet Declarations
            UIVariables.CometName = self.CometNameBox.text()
            UIVariables.Rh = self.RHBox.text()
            UIVariables.CometDelta = self.DeltaComBox.text()
            UIVariables.TransformMethod = self.TFMethBox.text()
            if(self.TFApplied.isChecked == True):
                UIVariables.ApplyTransforMethod = True
            else:
                UIVariables.ApplyTransforMethod = False

            #Grid Declarations
            UIVariables.AngularPoints = self.APointsBox.text()
            UIVariables.RadialPoints = self.RadPointsBox.text()
            UIVariables.RadialSubsteps = self.RadSubBox.text()

            #Extra Declarations
            if(self.BinTimesBox.isChecked() == True):
                UIVariables.PrintBinnedTimes = True
            else:
                UIVariables.PrintBinnedTimes = False
            if(self.ColumDBox.isChecked() == True):
                UIVariables.PrintColumnDensity = True
            else:
                UIVariables.PrintColumnDensity = False
            if(self.PrintPBox.isChecked() == True):
                UIVariables.PrintProgress = True
            else:
                UIVariables.PrintProgress = False
            if(self.PrintRadDBox.isChecked() == True):
                UIVariables.PrintRadialDensity = True
            else:
                UIVariables.PrintRadialDensity = False
            if(self.PickleBox.isChecked() == True):
                UIVariables.PyvComaPickle = True
            else:
                UIVariables.PyvComaPickle = False
            if(self.DCenterBox.isChecked() == True):
                UIVariables.Show3dColumnDensityCentered = True
            else:
                UIVariables.Show3dColumnDensityCentered = False
            if(self.DNotCenterBox.isChecked() == True):
                UIVariables.Show3dColumnDensityOffCenter = True
            else:
                UIVariables.Show3dColumnDensityOffCenter = False
            if(self.AgreeCheck.isChecked() == True):
                UIVariables.ShowAgreementCheck = True
            else:
                UIVariables.ShowAgreementCheck = False
            if(self.ApeCheck.isChecked() == True):
                UIVariables.ShowApertureChecks = True
            else:
                UIVariables.ShowApertureChecks = False
            if(self.ColumPlotBox.isChecked() == True):
                UIVariables.ShowColumnDensityPlots = True
            else:
                UIVariables.ShowColumnDensityPlots = False
            if(self.FragSputBox.isChecked() == True):
                UIVariables.ShowFragmentSputter = True
            else:
                UIVariables.ShowFragmentSputter = False
            if(self.RadPlotBox.isChecked() == True):
                UIVariables.ShowRadialPlots = True
            else:
                UIVariables.ShowRadialPlots = False

            #Runs the program
            runManualProgram()
            self.successRun()
            return
        
        if(self.FileInputBox.isChecked() == True):
            UIVariables.FileInputs = True
            runFileProgram()
            self.successRun()
            return
        if(self.ManInputBox.isChecked() == False and self.FileInputBox.isChecked() == False):
            self.noInput()
            return
    
    #File Input UI.
    #Creates an array of the user selected file names and copies it to UIVariables.py.
    def fileInp(self):
        self.fileOut.clear()
        UIVariables.FileArray = []
        files = QFileDialog.getOpenFileNames(self, 'Open file', '', 'Yaml files (*.yaml)')[0]
        i = 0
        while i < len(files):
            self.fileOut.addItem(files[i])
            UIVariables.FileArray.append(files[i])
            i += 1
        return
    
    #References the More() above when the More Infomation button is pressed.
    def moreInfo(self, checked):
        self.Win = MoreWindow()
        self.Win.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = App()
    Win.show()
    sys.exit(app.exec_())