#Driver program to create a UI to read in vectorial model data for comet analysis.
#Uses PyQt5 as the interface to create the UI.
#This work is based on a pvvectorial repository created by sjoset.
#
#Author: Jacob Duffy
#Version: 7/7/2022

import UIVariables
import FileRunner
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QListWidget, QTabWidget
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QLabel, QCheckBox, QFileDialog, QScrollBar, QVBoxLayout
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

#Class that defines a MatPlotLib object that is used in ResultsWindow.
class MatPlotLib(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        plot = Figure(figsize=(width, height), dpi=dpi)
        self.axes = plot.add_subplot(111)
        super(MatPlotLib, self).__init__(plot)

#Results window.
#Class to give a pop up window with the results from FileRunner.py using MatPlotLib.
class ResultsWindow(QWidget):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'Result Plots'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 1200
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.FragSput = QWidget()
        self.Radial = QWidget()
        self.ColumD = QWidget()
        self.ColumD3 = QWidget()
        self.ColumD3C = QWidget()

        #Graphs and plots for manual inputs
        if(UIVariables.ManInputs):

            #Plots and displays the fragment sputter graph
            if(UIVariables.ShowFragmentSputter):
                self.tabs.addTab(self.FragSput, "Fragment Sputter")
                self.FragSput.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [10,1,20,3,40])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.FragSput.layout.addWidget(self.graph)
                self.FragSput.layout.addWidget(self.toolbar)
                self.FragSput.setLayout(self.FragSput.layout)
        
            #Plots and displays the radial plot graph
            if(UIVariables.ShowRadialPlots):
                self.tabs.addTab(self.Radial, "Radial")
                self.Radial.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [-10,-1,-20,-3,-40])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.Radial.layout.addWidget(self.graph)
                self.Radial.layout.addWidget(self.toolbar)
                self.Radial.setLayout(self.Radial.layout)
        
            #Plots and displays the column density graph
            if(UIVariables.ShowColumnDensityPlots):
                self.tabs.addTab(self.ColumD, "Column Density")
                self.ColumD.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [0,1,2,3,4])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD.layout.addWidget(self.graph)
                self.ColumD.layout.addWidget(self.toolbar)
                self.ColumD.setLayout(self.ColumD.layout)
        
            #Plots and displays the column density graph (off centered)
            if(UIVariables.Show3dColumnDensityOffCenter):
                self.tabs.addTab(self.ColumD3, "Column Density (3D Off Centered)")
                self.ColumD3.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [0,-1,-2,-3,-4])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD3.layout.addWidget(self.graph)
                self.ColumD3.layout.addWidget(self.toolbar)
                self.ColumD3.setLayout(self.ColumD3.layout)
        
            #Plots and displays the column density graph (centered)
            if(UIVariables.Show3dColumnDensityCentered):
                self.tabs.addTab(self.ColumD3C, "Column Density (3D Centered)")
                self.ColumD3C.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [100,10,200,30,400])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD3C.layout.addWidget(self.graph)
                self.ColumD3C.layout.addWidget(self.toolbar)
                self.ColumD3C.setLayout(self.ColumD3C.layout)
        
        #Graph and plots for file input
        elif(UIVariables.FileInputs):

            #Plots and displays the fragment sputter graph
            if(UIVariables.ShowFragmentSputter):
                self.tabs.addTab(self.FragSput, "Fragment Sputter")
                self.FragSput.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [10,1,20,3,40])
                self.graph.axes.plot([0,1,2,3,4], [-10,-1,-20,-3,-40])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.FragSput.layout.addWidget(self.graph)
                self.FragSput.layout.addWidget(self.toolbar)
                self.FragSput.setLayout(self.FragSput.layout)
        
            #Plots and displays the radial plot graph
            if(UIVariables.ShowRadialPlots):
                self.tabs.addTab(self.Radial, "Radial")
                self.Radial.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [0,1,2,3,4])
                self.graph.axes.plot([0,1,2,3,4], [-10,-1,-20,-3,-40])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.Radial.layout.addWidget(self.graph)
                self.Radial.layout.addWidget(self.toolbar)
                self.Radial.setLayout(self.Radial.layout)
        
            #Plots and displays the column density graph
            if(UIVariables.ShowColumnDensityPlots):
                self.tabs.addTab(self.ColumD, "Column Density")
                self.ColumD.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [0,1,2,3,4])
                self.graph.axes.plot([0,1,2,3,4], [100,10,200,30,400])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD.layout.addWidget(self.graph)
                self.ColumD.layout.addWidget(self.toolbar)
                self.ColumD.setLayout(self.ColumD.layout)
        
            #Plots and displays the column density graph (off centered)
            if(UIVariables.Show3dColumnDensityOffCenter):
                self.tabs.addTab(self.ColumD3, "Column Density (3D Off Centered)")
                self.ColumD3.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [10,1,20,3,40])
                self.graph.axes.plot([0,1,2,3,4], [0,-1,-2,-3,-4])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD3.layout.addWidget(self.graph)
                self.ColumD3.layout.addWidget(self.toolbar)
                self.ColumD3.setLayout(self.ColumD3.layout)
        
            #Plots and displays the column density graph (centered)
            if(UIVariables.Show3dColumnDensityCentered):
                self.tabs.addTab(self.ColumD3C, "Column Density (3D Centered)")
                self.ColumD3C.layout = QVBoxLayout(self)
                self.graph = MatPlotLib(self, width=5, height=4, dpi=100)
                self.graph.axes.plot([0,1,2,3,4], [0,-1,-2,-3,-4])
                self.graph.axes.plot([0,1,2,3,4], [100,10,200,30,400])
                self.toolbar = NavigationToolbar2QT(self.graph, self)
                self.ColumD3C.layout.addWidget(self.graph)
                self.ColumD3C.layout.addWidget(self.toolbar)
                self.ColumD3C.setLayout(self.ColumD3C.layout)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        return
        

#Class to give a new pop up window to the user more info about proper usage of the Main UI.
class MoreWindow(QWidget):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'More Information'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 900
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QLabel("Inputs", self)
        self.label.setFont((QFont('Arial', 18)))
        self.label.move(450,20)
        self.inputText1 = QLabel("---All name inputs (parent, fragment, and comet) are optional inputs.", self)
        self.inputText1.move(20,100)
        self.inputText2 = QLabel("---Delta under \"comet variables\" is optional as it does not influence the results.", self)
        self.inputText2.move(20,150)
        self.inputText2 = QLabel("---In using a manual input, a .yaml file is created, \"keeping the .yaml file\" will", self)
        self.inputText2.move(20,200)
        self.inputText3 = QLabel("save to your current directory named \"pyvectorial.yaml\".", self)
        self.inputText3.move(20,230)
        self.inputText4 = QLabel("---\"Transformation method\" and \"time variation type\"", self)
        self.inputText4.move(20,280)
        self.inputText5 = QLabel("can only have 1 applied max.", self)
        self.inputText5.move(20,310)
        self.inputText6 = QLabel("---All other manual inputs can only be floats (grid variables must be int).", self)
        self.inputText6.move(20,360)
        self.inputText7 = QLabel("---File inputs will only be able to be .yaml files formatted the proper way.", self)
        self.inputText7.move(20,410)
        self.inputText8 = QLabel("(look at a manually created .yaml file for this format).", self)
        self.inputText8.move(20,440)
        self.label1 = QLabel("Other Information", self)
        self.label1.setFont((QFont('Arial', 18)))
        self.label1.move(350,540)
        self.otherText1 = QLabel("---In the running of the program, a .vmr file is created", self)
        self.otherText1.move(20,640)
        self.otherText2 = QLabel("and can be downloaded using the \"File Download\" selection box.", self)
        self.otherText2.move(20,670)
        self.otherText3 = QLabel("---The \"Pvy coma pickle\" is", self)
        self.otherText3.move(20,720)
        self.label2 = QLabel("*This program was created by Jacob Duffy at Auburn University Physics Department", self)
        self.label2.setFont((QFont('Arial', 5)))
        self.label2.move(500,880)
        self.show()

#Main UI Window, Driver Class. 
#Used to create/format the UI, read/test in all user data into UIVariables.py,
#reference other child UI windows, run the program and create a new window with the results.
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

        #UI Element creator

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
        
        #Creates manual input UI elements for the Production section
        self.textPro = QLabel("Production Variables", self)
        self.textPro.setFont((QFont('Arial', 12)))
        self.textPro.move(50,160)
        self.textPro.resize(400,40)
        self.BaseQText = QLabel("Input Base Q: ", self)
        self.BaseQText.move(20,220)
        self.BaseQText.resize(180,40)
        self.BaseQBox = QLineEdit(self)
        self.BaseQBox.move(200,220)
        self.BaseQBox.resize(180,40)
        self.BaseQUnits = QLabel("prod/sec", self)
        self.BaseQUnits.move(400,220)
        self.BaseQUnits.resize(180,40)
        self.TimeTVText = QLabel("*Time Variation Type: ", self)
        self.TimeTVText.move(20,280)
        self.TimeTVText.resize(400,40)
        self.TimeTVBox1 = QCheckBox("Sine", self)
        self.TimeTVBox1.setChecked(False)
        self.TimeTVBox1.move(290,280)
        self.TimeTVBox1.resize(400,40)
        self.TimeTVBox2 = QCheckBox("Gaussian", self)
        self.TimeTVBox2.setChecked(False)
        self.TimeTVBox2.move(395,280)
        self.TimeTVBox2.resize(400,40)
        self.TimeTVBox3 = QCheckBox("Square", self)
        self.TimeTVBox3.setChecked(False)
        self.TimeTVBox3.move(565,280)
        self.TimeTVBox3.resize(400,40)
        self.TimeTVBox4 = QCheckBox("None", self)
        self.TimeTVBox4.setChecked(True)
        self.TimeTVBox4.move(700,280)
        self.TimeTVBox4.resize(400,40)
        self.AmpText = QLabel("Input Amplitude: ", self)
        self.AmpText.move(20,340)
        self.AmpText.resize(400,40)
        self.AmpBox = QLineEdit(self)
        self.AmpBox.move(240,340)
        self.AmpBox.resize(180,40)
        self.AmpUnits = QLabel("molecules/sec", self)
        self.AmpUnits.move(440,340)
        self.AmpUnits.resize(180,40)
        self.ParamDeltaText = QLabel("Input Delta: ", self)
        self.ParamDeltaText.move(20,400)
        self.ParamDeltaText.resize(400,40)
        self.ParamDeltaUnits = QLabel("angular offset per hour", self)
        self.ParamDeltaUnits.move(380,400)
        self.ParamDeltaUnits.resize(400,40)
        self.ParamDeltaBox = QLineEdit(self)
        self.ParamDeltaBox.move(180,400)
        self.ParamDeltaBox.resize(180,40)
        self.PeriodText = QLabel("Input Period: ", self)
        self.PeriodText.move(20,460)
        self.PeriodText.resize(400,40)
        self.PeriodBox = QLineEdit(self)
        self.PeriodBox.move(190,460)
        self.PeriodBox.resize(180,40)
        self.PeriodUnits = QLabel("period/hour", self)
        self.PeriodUnits.move(390,460)
        self.PeriodUnits.resize(400,40)

        #Creates manual input UI elements for the Parent section
        self.textPar = QLabel("Parent Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(50,560)
        self.textPar.resize(400,40)
        self.ParNameText = QLabel("*Input Parent Name: ", self)
        self.ParNameText.move(20,620)
        self.ParNameText.resize(300,40)
        self.ParNameBox = QLineEdit(self)
        self.ParNameBox.move(270,620)
        self.ParNameBox.resize(180,40)
        self.OutVText = QLabel("Input Outflow Velocity: ", self)
        self.OutVText.move(20,680)
        self.OutVText.resize(300,40)
        self.OutVBox = QLineEdit(self)
        self.OutVBox.move(300,680)
        self.OutVBox.resize(180,40)
        self.OutVUnits = QLabel("km/hour", self)
        self.OutVUnits.move(500,680)
        self.OutVUnits.resize(300,40)
        self.TauDText = QLabel("Input Tau_D: ", self)
        self.TauDText.move(20,740)
        self.TauDText.resize(300,40)
        self.TauDBox = QLineEdit(self)
        self.TauDBox.move(185,740)
        self.TauDBox.resize(180,40)
        self.TauDUnits = QLabel("sec", self)
        self.TauDUnits.move(385,740)
        self.TauDUnits.resize(300,40)
        self.TauTParText = QLabel("Input Tau_T: ", self)
        self.TauTParText.move(20,800)
        self.TauTParText.resize(300,40)
        self.TauTParUnits = QLabel("sec", self)
        self.TauTParUnits.move(385,800)
        self.TauTParUnits.resize(300,40)
        self.TauTParBox = QLineEdit(self)
        self.TauTParBox.move(185,800)
        self.TauTParBox.resize(180,40)
        self.SigmaText = QLabel("Input Sigma: ", self)
        self.SigmaText.move(20,860)
        self.SigmaText.resize(300,40)
        self.SigmaBox = QLineEdit(self)
        self.SigmaBox.move(185,860)
        self.SigmaBox.resize(180,40)
        self.SigmaUnits = QLabel("cm^2", self)
        self.SigmaUnits.move(385,860)
        self.SigmaUnits.resize(300,40)
        self.T_DText = QLabel("Input T to D Ratio: ", self)
        self.T_DText.move(20,920)
        self.T_DText.resize(300,40)
        self.T_DBox = QLineEdit(self)
        self.T_DBox.move(250,920)
        self.T_DBox.resize(180,40) 

        #Creates manual input UI elements for the Fragment section  
        self.textFrag = QLabel("Fragment Variables", self)
        self.textFrag.setFont((QFont('Arial', 12)))
        self.textFrag.move(50,1020)
        self.textFrag.resize(400,40) 
        self.FragNameText = QLabel("*Input Fragment Name: ", self)
        self.FragNameText.move(20,1080)
        self.FragNameText.resize(300,40)
        self.FragNameBox = QLineEdit(self)
        self.FragNameBox.move(310,1080)
        self.FragNameBox.resize(180,40)  
        self.VPhotoText = QLabel("Input VPhoto: ", self)
        self.VPhotoText.move(20,1140)
        self.VPhotoText.resize(300,40)
        self.VPhotoBox = QLineEdit(self)
        self.VPhotoBox.move(190,1140)
        self.VPhotoBox.resize(180,40)
        self.VPhotoUnits = QLabel("sec", self)
        self.VPhotoUnits.move(390,1140)
        self.VPhotoUnits.resize(300,40)
        self.TauTFragText = QLabel("Input Tau_T: ", self)
        self.TauTFragText.move(20,1200)
        self.TauTFragText.resize(300,40)
        self.TauTFragBox = QLineEdit(self)
        self.TauTFragBox.move(185,1200)
        self.TauTFragBox.resize(180,40)    
        self.TauTFragUnits = QLabel("sec", self)
        self.TauTFragUnits.move(385,1200)
        self.TauTFragUnits.resize(300,40)

        #Creates manual input UI elements for the Comet section
        self.textPar = QLabel("Comet Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(880,160)
        self.textPar.resize(400,40)
        self.CometNameText = QLabel("*Input Comet Name: ", self)
        self.CometNameText.move(850,220)
        self.CometNameText.resize(300,40)
        self.CometNameBox = QLineEdit(self)
        self.CometNameBox.move(1110,220)
        self.CometNameBox.resize(180,40) 
        self.RHText = QLabel("Input Rh: ", self)
        self.RHText.move(850,280)
        self.RHText.resize(300,40)
        self.RHBox = QLineEdit(self)
        self.RHBox.move(980,280)
        self.RHBox.resize(180,40)
        self.RHUnits = QLabel("AU", self)
        self.RHUnits.move(1180,280)
        self.RHUnits.resize(300,40)
        self.DeltaComText = QLabel("*Input Delta: ", self)
        self.DeltaComText.move(850,340)
        self.DeltaComText.resize(300,40)
        self.DeltaComBox = QLineEdit(self)
        self.DeltaComBox.move(1000,340)
        self.DeltaComBox.resize(180,40)
        self.TFMethText = QLabel("*Transformation Method: ", self)
        self.TFMethText.move(850,400)
        self.TFMethText.resize(450,40)
        self.TFApplied1 = QCheckBox("Cochran", self)
        self.TFApplied1.setChecked(False)
        self.TFApplied1.move(1170,400)
        self.TFApplied1.resize(450,40)
        self.TFApplied2 = QCheckBox("Fortran", self)
        self.TFApplied2.setChecked(False)
        self.TFApplied2.move(1330,400)
        self.TFApplied2.resize(450,40)
        self.TFApplied3 = QCheckBox("None", self)
        self.TFApplied3.setChecked(True)
        self.TFApplied3.move(1480,400)
        self.TFApplied3.resize(450,40)        

        #Creates manual input UI elements for the Grid section
        self.textGrid = QLabel("Grid Variables", self)
        self.textGrid.setFont((QFont('Arial', 12)))
        self.textGrid.move(880,500)
        self.textGrid.resize(400,40)
        self.APointsText = QLabel("Input Angular Points: ", self)
        self.APointsText.move(850,560)
        self.APointsText.resize(450,40)
        self.APointsBox = QLineEdit(self)
        self.APointsBox.move(1115,560)
        self.APointsBox.resize(180,40)
        self.RadPointsText = QLabel("Input Radial Points: ", self)
        self.RadPointsText.move(850,620)
        self.RadPointsText.resize(450,40)
        self.RadPointsBox = QLineEdit(self)
        self.RadPointsBox.move(1110,620)
        self.RadPointsBox.resize(180,40)
        self.RadSubText = QLabel("Input Radial Substeps: ", self)
        self.RadSubText.move(850,680)
        self.RadSubText.resize(450,40)
        self.RadSubBox = QLineEdit(self)
        self.RadSubBox.move(1130,680)
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
        self.RadPlotBox = QCheckBox("Show Radial Plots", self)
        self.RadPlotBox.setChecked(False)
        self.RadPlotBox.move(1610,350)
        self.RadPlotBox.resize(500,40)
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
        self.PickleBox = QPushButton("*Upload Pyv Coma Pickle", self)
        self.PickleBox.move(1610,770)
        self.PickleBox.resize(400,40)
        self.PickleBox.clicked.connect(self.pickleInp)
        self.pickleOut = QListWidget(self)
        self.pickleOut.setGeometry(60,400,400,60)
        self.pickleOut.move(1610,830)

        #Creates other UI elements such as certain check boxes/text and other UI stuff
        self.FileInputBox = QCheckBox("*Select for File Inputs", self)
        self.FileInputBox.setChecked(False)
        self.FileInputBox.move(870,1040)
        self.FileInputBox.resize(500,40)
        self.ManInputBox = QCheckBox("Select for Manual Inputs", self)
        self.ManInputBox.setChecked(False)
        self.ManInputBox.move(540,100)
        self.ManInputBox.resize(500,40)
        self.DownInputBox = QCheckBox("*Select for File Downloads", self)
        self.DownInputBox.setChecked(False)
        self.DownInputBox.move(1620,1040)
        self.DownInputBox.resize(500,40)
        self.KeepFile = QCheckBox("*Keep Created .yaml File", self)
        self.KeepFile.setChecked(False)
        self.KeepFile.move(850,840)
        self.KeepFile.resize(500,40)
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
        self.download = QPushButton('Select Download Folder', self)
        self.download.move(1620,1100)
        self.download.resize(400,40)
        self.download.clicked.connect(self.downInp)
        self.downloadOut = QListWidget(self)
        self.downloadOut.setGeometry(60,400,400,60)
        self.downloadOut.move(1620,1160)
        self.fileOut = QListWidget(self)
        self.fileOut.setGeometry(200, 400, 400, 200)
        self.fileOut.move(870,1160)
        self.scrollBar = QScrollBar(self)
        self.fileOut.setVerticalScrollBar(self.scrollBar)

        self.show()

    #Error Throws

    #No input type is selected by the user (either manual or file)
    def noInput(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("No input type selected. Please try again.")
        self.message.show()
    
    #File input has a data type that throws an exception
    def incorrectFile(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("A .yaml file has an incorrect data entry. Please try again.")
        self.message.show()
    
    #File input has a data type that throws an exception
    def noFileUploaded(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText("A .yaml file has not been selected. Please try again.")
        self.message.show()
    
    #Gave an incorrect data type for the manual data entry (almost always string could not
    #be converted to a float/int)
    def incorrectDataType(self, input):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText(f"Incorrect manual data entry for: \"{input}\". Please try again.")
        self.message.show()
    
    #Selected too many boxes for an input that only allowed for one
    def tooManyBoxes(self, input):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowTitle("Error")
        self.message.setText(f"Too many input boxes selected for: \"{input}\". Please try again.")
        self.message.show()
    
    #Program ran successfully, there should not be any errors
    def successRun(self):
        self.message = QMessageBox()
        self.message.setIcon(QMessageBox.Information)
        self.message.setWindowTitle("Success")
        self.message.setText("Program run successful!")
        self.message.show()
    
    #Test user input to see if it is a float
    def testFloat(self, input):
        try:
            float(input)
            if(float(input) >= 0):
                return True
            else:
                return False
        except ValueError:
            return False
    
    #Test user input ot see if it is an int
    def testInt(self, input):
        try:
            int(input)
            if(int(input) >= 0):
                return True
            else:
                return True
        except ValueError:
            return False


    #File Path References

    #Gets the path for where the user will download the results.
    def downInp(self):
        self.downloadOut.clear()
        UIVariables.DownloadFilePath = None
        path = QFileDialog.getExistingDirectory(self, 'Open directory')
        self.downloadOut.addItem(path)
        UIVariables.DownloadFilePath = path
        return
    
    #Gets the name/file path of the pickle file.
    def pickleInp(self):
        self.pickleOut.clear()
        UIVariables.PyvComaPickle = None
        file = QFileDialog.getOpenFileNames(self, 'Open file', '', 'Yaml files (*.yaml)')[0]
        i = 0
        while i < len(file):
            self.pickleOut.addItem(file[i])
            UIVariables.PyvComaPickle = file[i]
            i += 1
        return

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

    #Extra methods
    
    #References the More() above when the More Infomation button is pressed.
    def moreInfo(self, checked):
        self.Win = MoreWindow()
        self.Win.show()
    
    #Method to set the global variables in UIVariables.py for the "extra" catagory in the UI.
    def extraDec(self):
            if(self.BinTimesBox.isChecked()):
                UIVariables.PrintBinnedTimes = True
            else:
                UIVariables.PrintBinnedTimes = False
            if(self.ColumDBox.isChecked()):
                UIVariables.PrintColumnDensity = True
            else:
                UIVariables.PrintColumnDensity = False
            if(self.PrintPBox.isChecked()):
                UIVariables.PrintProgress = True
            else:
                UIVariables.PrintProgress = False
            if(self.PrintRadDBox.isChecked()):
                UIVariables.PrintRadialDensity = True
            else:
                UIVariables.PrintRadialDensity = False
            if(self.DCenterBox.isChecked()):
                UIVariables.Show3dColumnDensityCentered = True
            else:
                UIVariables.Show3dColumnDensityCentered = False
            if(self.DNotCenterBox.isChecked()):
                UIVariables.Show3dColumnDensityOffCenter = True
            else:
                UIVariables.Show3dColumnDensityOffCenter = False
            if(self.AgreeCheck.isChecked()):
                UIVariables.ShowAgreementCheck = True
            else:
                UIVariables.ShowAgreementCheck = False
            if(self.ApeCheck.isChecked()):
                UIVariables.ShowApertureChecks = True
            else:
                UIVariables.ShowApertureChecks = False
            if(self.ColumPlotBox.isChecked()):
                UIVariables.ShowColumnDensityPlots = True
            else:
                UIVariables.ShowColumnDensityPlots = False
            if(self.FragSputBox.isChecked()):
                UIVariables.ShowFragmentSputter = True
            else:
                UIVariables.ShowFragmentSputter = False
            if(self.RadPlotBox.isChecked()):
                UIVariables.ShowRadialPlots = True
            else:
                UIVariables.ShowRadialPlots = False
        
    #Run Program button
    def runProg(self):
        UIVariables.ManInputs = False
        UIVariables.FileInputs = False

        #Manual input runner
        #Test proper user input and assigns the results to global variables in UIVariables.py
        #Throws errors if user input is not correct
        if(self.ManInputBox.isChecked()):
            UIVariables.ManInputs = True

            #Param Declarations
            if(self.testFloat(self.BaseQBox.text())):
                UIVariables.BaseQ = float(self.BaseQBox.text())
            else:
                self.incorrectDataType("Base Q")
                return
            if((self.TimeTVBox1.isChecked() == True) 
                and (self.TimeTVBox2.isChecked() == False)
                and (self.TimeTVBox3.isChecked() == False)
                and (self.TimeTVBox4.isChecked() == False)):
                UIVariables.TimeVariationType = "sine wave"
            elif((self.TimeTVBox1.isChecked() == False) 
                and (self.TimeTVBox2.isChecked() == True)
                and (self.TimeTVBox3.isChecked() == False)
                and (self.TimeTVBox4.isChecked() == False)):
                UIVariables.TimeVariationType = "gaussian"
            elif((self.TimeTVBox1.isChecked() == False) 
                and (self.TimeTVBox2.isChecked() == False)
                and (self.TimeTVBox3.isChecked() == True)
                and (self.TimeTVBox4.isChecked() == False)):
                UIVariables.TimeVariationType = "square pulse"
            elif((self.TimeTVBox1.isChecked() == False) 
                and (self.TimeTVBox2.isChecked() == False)
                and (self.TimeTVBox3.isChecked() == False)
                and (self.TimeTVBox4.isChecked() == True)):
                UIVariables.TimeVariationType = None
            else:
                self.tooManyBoxes("Time Variation Type")
                return
            if(self.testFloat(self.AmpBox.text())):
                UIVariables.Amplitude = float(self.AmpBox.text())
            else:
                self.incorrectDataType("Amplitude")
                return
            if(self.testFloat(self.ParamDeltaBox.text())):
                UIVariables.ParamDelta = float(self.ParamDeltaBox.text())
            else:
                self.incorrectDataType("Delta")
                return
            if(self.testFloat(self.PeriodBox.text())):
                UIVariables.Period = float(self.PeriodBox.text())
            else:
                self.incorrectDataType("Period")
                return

            #Parent Declarations
            UIVariables.ParentName = self.ParNameBox.text()
            if(self.testFloat(self.OutVBox.text())):
                UIVariables.VOutflow = float(self.OutVBox.text())
            else:
                self.incorrectDataType("Outflow Velocity")
                return
            if(self.testFloat(self.TauDBox.text())):
                UIVariables.TauD = float(self.TauDBox.text())
            else:
                self.incorrectDataType("Tau_D")
                return
            if(self.testFloat(self.TauTParBox.text())):
                UIVariables.TauTParent = float(self.TauTParBox.text())
            else:
                self.incorrectDataType("Tau_T")
                return
            if(self.testFloat(self.SigmaBox.text())):
                UIVariables.Sigma = float(self.SigmaBox.text())
            else:
                self.incorrectDataType("Sigma")
                return
            if(self.testFloat(self.T_DBox.text())):
                UIVariables.TtoDRatio = float(self.T_DBox.text())
            else:
                self.incorrectDataType("T to D Ratio")
                return

            #Fragment Declarations
            UIVariables.FragmentName = self.FragNameBox.text()
            if(self.testFloat(self.VPhotoBox.text())):
                UIVariables.VPhoto = float(self.VPhotoBox.text())
            else:
                self.incorrectDataType("VPhoto")
                return
            if(self.testFloat(self.TauTFragBox.text())):
                UIVariables.TauTFragment = float(self.TauTFragBox.text())
            else:
                self.incorrectDataType("Tau_T")
                return

            #Comet Declarations
            UIVariables.CometName = self.CometNameBox.text()
            if(self.testFloat(self.RHBox.text())):
                UIVariables.Rh = float(self.RHBox.text())
            else:
                self.incorrectDataType("Rh")
                return
            UIVariables.CometDelta = self.DeltaComBox.text()
            if((self.TFApplied1.isChecked() == True)
                and (self.TFApplied2.isChecked() == False)
                and (self.TFApplied3.isChecked() == False)):
                UIVariables.TransformMethod = "cochran_schleicher_93"
                UIVariables.ApplyTransforMethod = True
            elif((self.TFApplied1.isChecked() == False)
                and (self.TFApplied2.isChecked() == True)
                and (self.TFApplied3.isChecked() == False)):
                UIVariables.TransformMethod = "festou_fortran"
                UIVariables.ApplyTransforMethod = True
            elif((self.TFApplied1.isChecked() == False)
                and (self.TFApplied2.isChecked() == False)
                and (self.TFApplied3.isChecked() == True)):
                UIVariables.TransformMethod = None
                UIVariables.ApplyTransforMethod = False
            else:
                self.tooManyBoxes("Transformation Method")
                return

            #Grid Declarations
            if(self.testInt(self.APointsBox.text())):
                UIVariables.AngularPoints = int(self.APointsBox.text())
            else:
                self.incorrectDataType("Angular Points")
                return
            if(self.testInt(self.RadPointsBox.text())):
                UIVariables.RadialPoints = int(self.RadPointsBox.text())
            else:
                self.incorrectDataType("Radial Points")
                return
            if(self.testInt(self.RadSubBox.text())):
                UIVariables.RadialSubsteps = int(self.RadSubBox.text())
            else:
                self.incorrectDataType("Radial Substeps")
                return
            
            #Runs the program
            self.extraDec()
            FileRunner.runManualProgram()
            self.successRun()
            if((UIVariables.ShowFragmentSputter == False)
            and (UIVariables.Show3dColumnDensityCentered == False) 
            and (UIVariables.Show3dColumnDensityOffCenter == False)
            and (UIVariables.ShowRadialPlots == False)
            and (UIVariables.ShowColumnDensityPlots == False)):
                return
            self.Win = ResultsWindow()
            self.Win.show()
            return
        
        #File input runner
        #Test to see if there is at least 1 correct .yaml file uploaded and reads the files
        #for correct format in FileRunner.py
        #Throws an error if any of the 2 test fail
        elif(self.FileInputBox.isChecked()):
            UIVariables.FileInputs = True

            #Test to see if there had been a file uploaded
            if (len(UIVariables.FileArray) == 0):
                self.noFileUploaded()
                return
            
            #Reads all files to see if they are all formatted properly        
            if (FileRunner.fileTest()):
                #Runs the program
                self.extraDec()
                FileRunner.runFileProgram()
                self.successRun()
                if((UIVariables.ShowFragmentSputter == False)
                and (UIVariables.Show3dColumnDensityCentered == False) 
                and (UIVariables.Show3dColumnDensityOffCenter == False)
                and (UIVariables.ShowRadialPlots == False)
                and (UIVariables.ShowColumnDensityPlots == False)):
                    return
                self.Win = ResultsWindow()
                self.Win.show()
            else:
                self.incorrectFile()
            return

        #Throws an exception if there is no input type selected
        else:
            self.noInput()
            return
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = App()
    Win.show()
    sys.exit(app.exec_())