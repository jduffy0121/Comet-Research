#Driver program to create a UI to read in vectorial model data for comet analysis
#and create multiple results graphs using MatPlotLib.
#Uses PyQt5 as the interface to create the UI.
#This work is based on a pvvectorial repository created by sjoset.
#
#Author: Jacob Duffy
#Version: 7/21/2022

import UIVariables
import FileCreator
import FileRunner
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QListWidget, QTabWidget, QScrollArea
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QLabel, QCheckBox, QFileDialog, QVBoxLayout, QRadioButton
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

#Plot the graphs
#Creates a MatPlotLib graph widget for ResultsWindow() based on the graphType input.
class PlotGraphs(FigureCanvasQTAgg):
    #Intial UI Config
    def __init__(self, vmc, vmr, graphType, parent=None, width=10, height=10, dpi=100):
        plot = Figure(figsize=(width, height), dpi=dpi) #Creates the figure
        self.axes = plot.add_subplot(111) #Creates the initial (x,y) axis
        FigureCanvasQTAgg.__init__(self, plot)
        self.vmc = vmc
        self.vmr = vmr
        self.graphType = graphType
        self.setParent(parent)
        self.graph()

    #Updates the graph figure that is created in __init__ to the correct graph based on graphType.
    def graph(self):
        if(self.graphType == "frag sput"):
            self.figure = FileRunner.getFragSputter(self.vmc, self.vmr)
        if(self.graphType == "radial"):
            self.figure = FileRunner.getRadialPlots(self.vmc, self.vmr)
        if(self.graphType == "column dens"):
            self.figure = FileRunner.getColumnDensity(self.vmc, self.vmr)
        if(self.graphType == "3d column dens"):
            self.figure = FileRunner.get3DColumnDensity(self.vmc, self.vmr)
        if(self.graphType == "3d column dens cent"):
            self.figure = FileRunner.get3DColumnDensityCentered(self.vmc, self.vmr)
        self.draw() #Draws the figure

#Extra results
#Creates a QWidget for radial/column densities and agreement/aperture checks for ResultsWindow()
class ExtraResults(QWidget):
    #Intial UI Config
    def __init__(self, vmr, parent=None):
        super().__init__(parent)
        self.vmr = vmr
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):
        self.radDensityResults = QLabel(f"{FileRunner.getPrintRadialDensity(self.vmr)}", self)
        self.radDensityResults.move(0,0)
        self.columnDensityResults = QLabel(f"{FileRunner.getPrintColumnDensity(self.vmr)}", self)
        self.columnDensityResults.move(600,30)
        self.agreementCheckResults = QLabel(f"{FileRunner.getAgreementCheck(self.vmr)}", self)
        self.agreementCheckResults.move(1200,30)

        #Test to see if pickle input was used as UIVariables.ApertureChecks == None if it was as
        #no coma object was created
        if (UIVariables.PickleInputs == False):
            self.agreementCheckResults = QLabel(f"{UIVariables.ApertureChecks}", self)
            self.agreementCheckResults.move(1200,200)

#Results window.
#Class to give a pop up window with the results from FileRunner.py using PlotGraphs().
class ResultsWindow(QWidget):
    #Intial UI Config
    def __init__(self, vmc, vmr, parent=None):
        super().__init__(parent)
        self.title = 'Results'
        self.left = 10
        self.top = 10
        self.width = 2500
        self.height = 1400
        self.vmc = vmc
        self.vmr = vmr
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Defines a special style format for Results() (for aesthetic purposes only)
        self.setStyleSheet("""
        QWidget{
            background: None
        }
        QLabel {
            color: #000000;
            background: None;
        }
        """)

        self.layout = QVBoxLayout() #Defines the full window layout
        self.tabs = QTabWidget() #Creates a widget containing the tabs

        #Creates a bunch of empty widgets used in each tab
        self.fragSput = QWidget() 
        self.radial = QWidget()
        self.columD = QWidget()
        self.columD3 = QWidget()
        self.columD3C = QWidget()

        #Plots and displays the fragment sputter graph
        self.tabs.addTab(self.fragSput, "Fragment Sputter") #Creates the tab named "Fragment Sputter"
        self.fragSput.layout = QVBoxLayout(self) #Defines the tab layout as "QVBoxLayout"
        self.fragSputGraph = PlotGraphs(self.vmc, self.vmr, "frag sput", width=5, height=4, dpi=100) #Creates the graph
        self.fragSputToolbar = NavigationToolbar2QT(self.fragSputGraph, self) #Creates the toolbar for the graph
        self.fragSput.layout.addWidget(self.fragSputGraph) #Adds the graph to the QVBoxLayout
        self.fragSput.layout.addWidget(self.fragSputToolbar) #Adds the toolbar to the QVBoxLayout
        self.fragSput.setLayout(self.fragSput.layout) #Finalizes the tab layout
        
        #Plots and displays the radial plot graph
        self.tabs.addTab(self.radial, "Radial")
        self.radial.layout = QVBoxLayout(self)
        self.radialGraph = PlotGraphs(self.vmc, self.vmr, "radial", width=5, height=4, dpi=100)
        self.radialToolbar = NavigationToolbar2QT(self.radialGraph, self)
        self.radial.layout.addWidget(self.radialGraph)
        self.radial.layout.addWidget(self.radialToolbar)
        self.radial.setLayout(self.radial.layout)
        
        #Plots and displays the column density graph
        self.tabs.addTab(self.columD, "Column Density")
        self.columD.layout = QVBoxLayout(self)
        self.columDGraph = PlotGraphs(self.vmc, self.vmr, "column dens", width=5, height=4, dpi=100)
        self.columDToolbar = NavigationToolbar2QT(self.columDGraph, self)
        self.columD.layout.addWidget(self.columDGraph)
        self.columD.layout.addWidget(self.columDToolbar)
        self.columD.setLayout(self.columD.layout)
        
        #Plots and displays the column density graph (off centered)
        self.tabs.addTab(self.columD3, "Column Density (3D Off Centered)")
        self.columD3.layout = QVBoxLayout(self)
        self.columD3Graph = PlotGraphs(self.vmc, self.vmr, "3d column dens", width=5, height=4, dpi=100)
        self.columD3Toolbar = NavigationToolbar2QT(self.columD3Graph, self)
        self.columD3.layout.addWidget(self.columD3Graph)
        self.columD3.layout.addWidget(self.columD3Toolbar)
        self.columD3.setLayout(self.columD3.layout)
        
        #Plots and displays the column density graph (centered)
        self.tabs.addTab(self.columD3C, "Column Density (3D Centered)")
        self.columD3C.layout = QVBoxLayout(self)
        self.columD3CGraph = PlotGraphs(self.vmc, self.vmr, "3d column dens cent", width=5, height=4, dpi=100)
        self.columD3CToolbar = NavigationToolbar2QT(self.columD3CGraph, self)
        self.columD3C.layout.addWidget(self.columD3CGraph)
        self.columD3C.layout.addWidget(self.columD3CToolbar)
        self.columD3C.setLayout(self.columD3C.layout)
    
        self.tabs.addTab(ExtraResults(self.vmr), "Extra") #Creates the extra tab by referencing ExtraResults()
        self.layout.addWidget(self.tabs) #Adds all tabs to the Results window
        self.setLayout(self.layout) #Finalizes the whole window layout
        
#Time Variation window.
#Class to give the user the option to add time variation in anthor window.
class TimeVarWindow(QWidget):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'Time Variation Method'
        self.left = 10
        self.top = 10
        self.width = 1450
        self.height = 710
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Defines a special style format for TimeVarWindow() (for aesthetic purposes only)
        self.setStyleSheet("""
        QWidget {
            background: #1F2022;
        }
        QListWidget {
            border: 2px solid #fff;
            padding: 10px;
            border-style: solid;
            border-radius: 10px;
            background: #3D3D3D; 
        }
        QLabel {
            color: #EEEADE;
            background: #3D3D3D;
        }   
        QLineEdit {
            padding: 1px;
            color: #EEEADE;
            border-style: solid;
            border: 1px solid #EEEADE;
            border-radius: 8px;
            background: #616161
        }
        QPushButton {
            padding: 1px;
            color: #EEEADE;
            border-style: solid;
            border: 1px solid #EEEADE;
            border-radius: 8px;
            background: #616161
        }
        QPushButton:hover {
            border: 1px #C6C6C6 solid;
            color: #fff;
            background: #0892D0;
        }  
        QRadioButton {
            background: None
        }  """)

        #Creates a bunch of UI Boxes (for aesthetic purposes only)
        self.uiBox1 = QListWidget(self)
        self.uiBox1.setGeometry(75,120,120,75)
        self.uiBox1.move(290,10)
        self.uiBox2 = QListWidget(self)
        self.uiBox2.setGeometry(185,675,675,185)
        self.uiBox2.move(10,110)
        self.uiBox3 = QListWidget(self)
        self.uiBox3.setGeometry(75,175,175,75)
        self.uiBox3.move(230,370)
        self.uiBox4 = QListWidget(self)
        self.uiBox4.setGeometry(185,675,675,185)
        self.uiBox4.move(10,470)
        self.uiBox5 = QListWidget(self)
        self.uiBox5.setGeometry(75,230,230,75)
        self.uiBox5.move(990,10)
        self.uiBox6 = QListWidget(self)
        self.uiBox6.setGeometry(185,650,650,185)
        self.uiBox6.move(790,110)
        self.uiBox7 = QListWidget(self)
        self.uiBox7.setGeometry(210,480,480,210)
        self.uiBox7.move(835,370)

        #Creates title headers for the UI
        self.headingLabel1 = QLabel("Sine", self)
        self.headingLabel1.setFont((QFont('Arial', 18)))
        self.headingLabel1.move(300,20)
        self.headingLabel2 = QLabel("Gaussian", self)
        self.headingLabel2.setFont((QFont('Arial', 18)))
        self.headingLabel2.move(1000,20)
        self.headingLabel3 = QLabel("Square", self)
        self.headingLabel3.setFont((QFont('Arial', 18)))
        self.headingLabel3.move(240,380)

        #Creates UI elements for sine input
        self.sineAmpText = QLabel("Input Amplitude: ", self)
        self.sineAmpText.move(20,120)
        self.sineAmpText.resize(300,40)
        self.sineAmpBox = QLineEdit(self)
        self.sineAmpBox.move(240,120)
        self.sineAmpBox.resize(180,40)
        self.sineAmpUnits = QLabel("molecules/sec", self)
        self.sineAmpUnits.move(430,120)
        self.sineAmpUnits.resize(200,40)
        self.sinePeriodText = QLabel("Input Period: ", self)
        self.sinePeriodText.move(20,180)
        self.sinePeriodText.resize(300,40)
        self.sinePeriodBox = QLineEdit(self)
        self.sinePeriodBox.move(200,180)
        self.sinePeriodBox.resize(180,40)
        self.sinePeriodUnits = QLabel("hours", self)
        self.sinePeriodUnits.move(390,180)
        self.sinePeriodUnits.resize(150,40)
        self.sineDeltaText = QLabel("Input Delta: ", self)
        self.sineDeltaText.move(20,240)
        self.sineDeltaText.resize(300,40)
        self.sineDeltaBox = QLineEdit(self)
        self.sineDeltaBox.move(190,240)
        self.sineDeltaBox.resize(180,40)
        self.sineDeltaUnits = QLabel("angular offset in hours", self)
        self.sineDeltaUnits.move(380,240)
        self.sineDeltaUnits.resize(300,40)

        #Creates UI elements for gaussian input
        self.gausAmpText = QLabel("Input Amplitude: ", self)
        self.gausAmpText.move(800,120)
        self.gausAmpText.resize(300,40)
        self.gausAmpBox = QLineEdit(self)
        self.gausAmpBox.move(1020,120)
        self.gausAmpBox.resize(180,40)
        self.gausAmpUnits = QLabel("molecules/sec", self)
        self.gausAmpUnits.move(1210,120)
        self.gausAmpUnits.resize(200,40)
        self.gausStdText = QLabel("Input Standard Deviation: ", self)
        self.gausStdText.move(800,180)
        self.gausStdText.resize(350,40)
        self.gausStdBox = QLineEdit(self)
        self.gausStdBox.move(1120,180)
        self.gausStdBox.resize(180,40)
        self.gausStdUnits = QLabel("hours", self)
        self.gausStdUnits.move(1310,180)
        self.gausStdUnits.resize(100,40)
        self.gausTPText = QLabel("Input Time at Peak: ", self)
        self.gausTPText.move(800,240)
        self.gausTPText.resize(350,40)
        self.gausTPBox = QLineEdit(self)
        self.gausTPBox.move(1045,240)
        self.gausTPBox.resize(180,40)
        self.gausTPUnits = QLabel("hours", self)
        self.gausTPUnits.move(1235,240)
        self.gausTPUnits.resize(150,40)

        #Creates UI elements for square input
        self.squareAmpText = QLabel("Input Amplitude: ", self)
        self.squareAmpText.move(20,480)
        self.squareAmpText.resize(300,40)
        self.squareAmpBox = QLineEdit(self)
        self.squareAmpBox.move(240,480)
        self.squareAmpBox.resize(180,40)
        self.squareAmpUnits = QLabel("molecules/sec", self)
        self.squareAmpUnits.move(430,480)
        self.squareAmpUnits.resize(200,40)
        self.squareDurText = QLabel("Input Duration: ", self)
        self.squareDurText.move(20,540)
        self.squareDurText.resize(300,40)
        self.squareDurBox = QLineEdit(self)
        self.squareDurBox.move(230,540)
        self.squareDurBox.resize(180,40)
        self.squareDurUnits = QLabel("hours", self)
        self.squareDurUnits.move(420,540)
        self.squareDurUnits.resize(150,40)
        self.squareTSPText = QLabel("Input Start of Pulse: ", self)
        self.squareTSPText.move(20,600)
        self.squareTSPText.resize(300,40)
        self.squareTSPBox = QLineEdit(self)
        self.squareTSPBox.move(280,600)
        self.squareTSPBox.resize(180,40)
        self.squareTSPUnits = QLabel("hours", self)
        self.squareTSPUnits.move(470,600)
        self.squareTSPUnits.resize(150,40)

        #Other UI elements
        self.setButton = QPushButton('Set Time Variation Method', self)
        self.setButton.move(860,630)
        self.setButton.resize(400,40)
        self.setButton.clicked.connect(self.setResults)
        self.sineButton = QRadioButton("", self)
        self.sineButton.move(850,380)
        self.sineButtonText = QLabel("Select for sine time variation", self)
        self.sineButtonText.move(885,380)
        self.gausButton = QRadioButton("", self)
        self.gausButton.move(850,430)
        self.gausButtonText = QLabel("Select for gaussian time variation", self)
        self.gausButtonText.move(885,430)
        self.squareButton = QRadioButton("", self)
        self.squareButton.move(850,480)
        self.gausButtonText = QLabel("Select for square time variation", self)
        self.gausButtonText.move(885,480)
        self.noneButton = QRadioButton("", self)
        self.noneButton.move(850,530)
        self.noneButton.setChecked(True)
        self.noneButtonText = QLabel("Select for no time variation", self)
        self.noneButtonText.move(885,530)
        self.show()
    
    #Creates pop up windows for successfully setting time variation or error throws
    def popUpWin(self, type, message=None):
        self.message = QMessageBox()
        if(type == 'success'):
            self.message.setIcon(QMessageBox.Information)
            self.message.setWindowTitle("Success")
            self.message.setText(f"Time variation successfully set to: \"{message}\".")
        else:
            self.message.setIcon(QMessageBox.Critical)
            self.message.setWindowTitle("Error")
            if(type == 'incorrect data'):
                 self.message.setText(f"Incorrect manual data entry for: \"{message}\". Please try again.")
        self.message.show()
    
    #Sets the current user input to the global variables in UIVariables.py
    def setResults(self):
        #Clears out any possible time variation type input that occured before
        UIVariables.TimeVariationType = None
        UIVariables.SinAmp = None
        UIVariables.SinDelta = None
        UIVariables.SinPer = None
        UIVariables.GausAmp = None
        UIVariables.GausSTD = None
        UIVariables.GausT_Max = None
        UIVariables.SquareAmp = None
        UIVariables.SquareDur = None
        UIVariables.SquareT_Start = None
       
        #Declarations if sine time variation is selected
        if(self.sineButton.isChecked()):
            UIVariables.TimeVariationType = 'sine wave'
            if(FileRunner.valueTest(self.sineAmpBox.text(), 'float')):
                UIVariables.SinAmp = float(self.sineAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.sinePeriodBox.text(), 'float')):
                UIVariables.SinPer = float(self.sinePeriodBox.text())
            else:
                self.popUpWin('incorrect data', 'Period')
                return
            if(FileRunner.valueTest(self.sineDeltaBox.text(), 'float')):
                UIVariables.SinDelta = float(self.sineDeltaBox.text())
            else:
                self.popUpWin('incorrect data', 'Delta')
                return
            self.popUpWin('success', 'Sine')
            return

        #Declarations if gaussian time variation is selected
        elif(self.gausButton.isChecked()):
            UIVariables.TimeVariationType = 'gaussian'
            if(FileRunner.valueTest(self.gausAmpBox.text(), 'float')):
                UIVariables.GausAmp = float(self.gausAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.gausStdBox.text(), 'float')):
                UIVariables.GausSTD = float(self.gausStdBox.text())
            else:
                self.popUpWin('incorrect data', 'Standard Deviation')
                return
            if(FileRunner.valueTest(self.gausTPBox.text(), 'float')):
                UIVariables.GausT_Max = float(self.gausTPBox.text())
            else:
                self.popUpWin('incorrect data', 'Time at Peak')
                return
            self.popUpWin('success', 'Gaussian')
            return

        #Declarations if square time variation is selected
        elif(self.squareButton.isChecked()):
            UIVariables.TimeVariationType = 'square pulse'
            if(FileRunner.valueTest(self.squareAmpBox.text(), 'float')):
                UIVariables.SquareAmp = float(self.squareAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.squareDurBox.text(), 'float')):
                UIVariables.SquareDur = float(self.squareDurBox.text())
            else:
                self.popUpWin('incorrect data', 'Duration')
                return
            if(FileRunner.valueTest(self.squareTSPBox.text(), 'float')):
                UIVariables.SquareT_Start = float(self.squareTSPBox.text())
            else:
                self.popUpWin('incorrect data', 'Start of Pulse')
                return
            self.popUpWin('success', 'Square')
            return
        
        #Declarations if no time variation is selected
        elif(self.noneButton.isChecked()):
            self.popUpWin('success', 'None')
            return

#Class to give a new pop up window to the user more info about proper usage of the Main UI.
class MoreWindow(QWidget):
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'More Information'
        self.left = 10
        self.top = 10
        self.width = 1050
        self.height = 1110
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Defines a special style format for More() (for aesthetic purposes only)
        self.setStyleSheet("""
        QWidget {
            background: #1F2022;
        }
        QListWidget {
            border: 2px solid #fff;
            padding: 10px;
            border-style: solid;
            border-radius: 10px;
            background: #3D3D3D; 
        }
        QLabel {
            color: #EEEADE;
            background: #3D3D3D;
        } """)

        #Creates a bunch of UI Boxes (for aesthetic purposes only)
        self.uiBox1 = QListWidget(self)
        self.uiBox1.setGeometry(75,165,165,75)
        self.uiBox1.move(435,10)
        self.uiBox2 = QListWidget(self)
        self.uiBox2.setGeometry(480,1000,1000,480)
        self.uiBox2.move(25,115)
        self.uiBox3 = QListWidget(self)
        self.uiBox3.setGeometry(75,195,195,75)
        self.uiBox3.move(435,640)
        self.uiBox4 = QListWidget(self)
        self.uiBox4.setGeometry(340,1000,1000,340)
        self.uiBox4.move(25,745)

        #Creates title headers for the UI
        self.headingLabel1 = QLabel("Inputs", self)
        self.headingLabel1.setFont((QFont('Arial', 18)))
        self.headingLabel1.move(450,20)
        self.headingLabel2 = QLabel("Outputs", self)
        self.headingLabel2.setFont((QFont('Arial', 18)))
        self.headingLabel2.move(450,650)

        #Input text
        self.inputText1 = QLabel("---All name inputs (parent, fragment, and comet) are optional inputs.", self)
        self.inputText1.move(40,130)
        self.inputText2 = QLabel("---Delta under \"comet variables\" is optional as it does not influence the results.", self)
        self.inputText2.move(40,180)
        self.inputText2 = QLabel("---In using a manual input, a .yaml file is created, \"keeping the .yaml file\" will", self)
        self.inputText2.move(40,230)
        self.inputText3 = QLabel("save to your current directory named \"pyvectorial.yaml\".", self)
        self.inputText3.move(40,260)
        self.inputText4 = QLabel("---\"Transformation method\" and \"time variation type\"", self)
        self.inputText4.move(40,310)
        self.inputText5 = QLabel("can only have 1 applied max.", self)
        self.inputText5.move(40,340)
        self.inputText6 = QLabel("---All other manual inputs can only be floats (grid variables must be int).", self)
        self.inputText6.move(40,390)
        self.inputText7 = QLabel("---A .yaml file will only be understood if it is formatted the proper way.", self)
        self.inputText7.move(40,440)
        self.inputText8 = QLabel("(look at a manually created .yaml file for this format).", self)
        self.inputText8.move(40,470)
        self.inputText9 = QLabel("---The \"Pvy coma pickle\" is a special file that will not create a vmc", self)
        self.inputText9.move(40,520)
        self.inputText10 = QLabel("when running the program as it already holds all important info from the vmc.", self)
        self.inputText10.move(40,550)

        #Output text
        self.outputText1 = QLabel ("---When finished the program will give the user:", self)
        self.outputText1.move(40,760)
        self.outputText2 = QLabel ("Fragment Sputter Graph", self)
        self.outputText2.move(180,800)
        self.outputText3 = QLabel ("Radial Density Graph", self)
        self.outputText3.move(180,840)
        self.outputText4 = QLabel ("Column Density Graphs (2D, 3D centered, 3D off centered)", self)
        self.outputText4.move(180,880)
        self.outputText5 = QLabel ("Radius vs. Fragment Densitiy Table", self)
        self.outputText5.move(180,920)
        self.outputText6 = QLabel ("Radius vs. Column Densitiy Table", self)
        self.outputText6.move(180,960)
        self.outputText7 = QLabel ("Fragment Agreement Check", self)
        self.outputText7.move(180,1000)
        self.outputText8 = QLabel ("Fragment Aperture Check (not given for pickle file input)", self)
        self.outputText8.move(180,1040)
        self.show()

#Main UI Window, Driver Class. 
#Used to create/format the UI, read/test in all user data into UIVariables.py,
#reference other child UI windows, run the program and create a new window with the results.
class App(QMainWindow): 
    #Intial UI Config
    def __init__(self,parent=None):
        super().__init__(parent)
        self.title = 'Vectorial Model Input UI' #Titles the UI window
        self.left = 10
        self.top = 10
        self.width = 1800 #Defines the size of the UI window
        self.height = 1100 #Defines the size of the UI window
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):

        #UI Element creator
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Creates a bunch of UI Boxes (for aesthetic purposes only)
        self.uiBox1 = QListWidget(self) #Creates a QListWidget() object
        self.uiBox1.setGeometry(925,1200,1200,925) #Defines the dimensions of the box
        self.uiBox1.move(15,145) #Moves the box to (x,y)
        self.uiBox2 = QListWidget(self)
        self.uiBox2.setGeometry(410,430,430,410)
        self.uiBox2.move(1335,145)
        self.uiBox3 = QListWidget(self)
        self.uiBox3.setGeometry(100,315,315,100)
        self.uiBox3.move(435,5)
        self.uiBox4 = QListWidget(self)
        self.uiBox4.setGeometry(100,250,250,100)
        self.uiBox4.move(1435,5)
        self.uiBox5 = QListWidget(self)
        self.uiBox5.setGeometry(270,430,430,270)
        self.uiBox5.move(1335,600)
        self.uiBox6 = QListWidget(self)
        self.uiBox6.setGeometry(160,325,325,160)
        self.uiBox6.move(1385,665)
        #Defines a special style format for uiBox6
        self.uiBox6.setStyleSheet("border: 1px solid #fff; padding: 10px; border-style: solid; color: #EEEADE; border-radius: 10px; background: #616161;") 

        #Creates title headers for the UI
        self.headingLabel1 = QLabel("Manual Input", self) #Creates a text box with the input string
        self.headingLabel1.move(450,20)
        self.headingLabel1.setFont((QFont('Arial', 18))) #Sets font to the input string and font size
        self.headingLabel1.resize(280,60) #Resize the text to fill up to the (x,y)
        self.headingLabel2 = QLabel("File Inputs", self)
        self.headingLabel2.move(1450,20)
        self.headingLabel2.setFont((QFont('Arial', 18)))
        self.headingLabel2.resize(225,60)
        
        #Creates manual input UI elements for the Production section
        self.textPro = QLabel("Production Variables", self)
        self.textPro.setFont((QFont('Arial', 12)))
        self.textPro.move(80,160)
        self.textPro.resize(400,40)
        self.baseQText = QLabel("Input Base Q: ", self)
        self.baseQText.move(50,220)
        self.baseQText.resize(180,40)
        self.baseQBox = QLineEdit(self) #Creates a textbox for user to input data in
        self.baseQBox.move(230,220)
        self.baseQBox.resize(180,40)
        self.baseQUnits = QLabel("prod/sec", self)
        self.baseQUnits.move(430,220)
        self.baseQUnits.resize(180,40)
        self.timeVarBox = QPushButton("*Select Time Variation Method", self)
        self.timeVarBox.move(50,280)
        self.timeVarBox.resize(400,40)
        self.timeVarBox.clicked.connect(self.timeVarWin) #Defines the method call when the button is clicked

        #Creates manual input UI elements for the Parent section
        self.textPar = QLabel("Parent Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(80,380)
        self.textPar.resize(400,40)
        self.parNameText = QLabel("*Input Parent Name: ", self)
        self.parNameText.move(50,440)
        self.parNameText.resize(300,40)
        self.parNameBox = QLineEdit(self)
        self.parNameBox.move(300,440)
        self.parNameBox.resize(180,40)
        self.outVText = QLabel("Input Outflow Velocity: ", self)
        self.outVText.move(50,500)
        self.outVText.resize(300,40)
        self.outVBox = QLineEdit(self)
        self.outVBox.move(330,500)
        self.outVBox.resize(180,40)
        self.outVUnits = QLabel("km/hour", self)
        self.outVUnits.move(530,500)
        self.outVUnits.resize(300,40)
        self.tauDText = QLabel("Input Tau_D: ", self)
        self.tauDText.move(50,560)
        self.tauDText.resize(300,40)
        self.tauDBox = QLineEdit(self)
        self.tauDBox.move(215,560)
        self.tauDBox.resize(180,40)
        self.tauDUnits = QLabel("sec", self)
        self.tauDUnits.move(415,560)
        self.tauDUnits.resize(300,40)
        self.tauTParText = QLabel("Input Tau_T: ", self)
        self.tauTParText.move(50,620)
        self.tauTParText.resize(300,40)
        self.tauTParUnits = QLabel("sec", self)
        self.tauTParUnits.move(415,620)
        self.tauTParUnits.resize(300,40)
        self.tauTParBox = QLineEdit(self)
        self.tauTParBox.move(215,620)
        self.tauTParBox.resize(180,40)
        self.sigmaText = QLabel("Input Sigma: ", self)
        self.sigmaText.move(50,680)
        self.sigmaText.resize(300,40)
        self.sigmaBox = QLineEdit(self)
        self.sigmaBox.move(215,680)
        self.sigmaBox.resize(180,40)
        self.sigmaUnits = QLabel("cm^2", self)
        self.sigmaUnits.move(415,680)
        self.sigmaUnits.resize(300,40)
        self.t_DText = QLabel("Input T to D Ratio: ", self)
        self.t_DText.move(50,740)
        self.t_DText.resize(300,40)
        self.t_DBox = QLineEdit(self)
        self.t_DBox.move(280,740)
        self.t_DBox.resize(180,40) 

        #Creates manual input UI elements for the Fragment section  
        self.textFrag = QLabel("Fragment Variables", self)
        self.textFrag.setFont((QFont('Arial', 12)))
        self.textFrag.move(80,840)
        self.textFrag.resize(400,40) 
        self.fragNameText = QLabel("*Input Fragment Name: ", self)
        self.fragNameText.move(50,900)
        self.fragNameText.resize(300,40)
        self.fragNameBox = QLineEdit(self)
        self.fragNameBox.move(340,900)
        self.fragNameBox.resize(180,40)  
        self.vPhotoText = QLabel("Input VPhoto: ", self)
        self.vPhotoText.move(50,960)
        self.vPhotoText.resize(300,40)
        self.vPhotoBox = QLineEdit(self)
        self.vPhotoBox.move(220,960)
        self.vPhotoBox.resize(180,40)
        self.vPhotoUnits = QLabel("km/hour", self)
        self.vPhotoUnits.move(420,960)
        self.vPhotoUnits.resize(300,40)
        self.tauTFragText = QLabel("Input Tau_T: ", self)
        self.tauTFragText.move(50,1020)
        self.tauTFragText.resize(300,40)
        self.tauTFragBox = QLineEdit(self)
        self.tauTFragBox.move(215,1020)
        self.tauTFragBox.resize(180,40)    
        self.tauTFragUnits = QLabel("sec", self)
        self.tauTFragUnits.move(415,1020)
        self.tauTFragUnits.resize(300,40)

        #Creates manual input UI elements for the Comet section
        self.textPar = QLabel("Comet Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(730,160)
        self.textPar.resize(400,40)
        self.cometNameText = QLabel("*Input Comet Name: ", self)
        self.cometNameText.move(700,220)
        self.cometNameText.resize(300,40)
        self.cometNameBox = QLineEdit(self)
        self.cometNameBox.move(960,220)
        self.cometNameBox.resize(180,40) 
        self.rHText = QLabel("Input Rh: ", self)
        self.rHText.move(700,280)
        self.rHText.resize(300,40)
        self.rHBox = QLineEdit(self)
        self.rHBox.move(830,280)
        self.rHBox.resize(180,40)
        self.rHUnits = QLabel("AU", self)
        self.rHUnits.move(1030,280)
        self.rHUnits.resize(150,40)
        self.deltaComText = QLabel("*Input Delta: ", self)
        self.deltaComText.move(700,340)
        self.deltaComText.resize(300,40)
        self.deltaComBox = QLineEdit(self)
        self.deltaComBox.move(870,340)
        self.deltaComBox.resize(180,40)
        self.tFMethText = QLabel("*Transformation Method: ", self)
        self.tFMethText.move(700,440)
        self.tFMethText.resize(450,40)
        self.tFApplied1 = QCheckBox("", self) #Set checkable box
        self.tFApplied1.setChecked(False) #Set checked box to be unchecked when the window is created
        self.tFApplied1.move(1020,400)
        self.tFApplied1.resize(150,40)
        self.tFApplied1Text = QLabel("Cochran", self)
        self.tFApplied1Text.resize(150,40)
        self.tFApplied1Text.move(1058,400)
        self.tFApplied2 = QCheckBox("", self)
        self.tFApplied2.setChecked(False)
        self.tFApplied2.move(1020,440)
        self.tFApplied2.resize(150,40)
        self.tFApplied2Text = QLabel("Fortran", self)
        self.tFApplied2Text.resize(150,40)
        self.tFApplied2Text.move(1058,440)
        self.tFApplied3 = QCheckBox("", self)
        self.tFApplied3.setChecked(True)
        self.tFApplied3.move(1020,480)
        self.tFApplied3.resize(150,40)   
        self.tFApplied3Text = QLabel("None", self)
        self.tFApplied3Text.resize(150,40)
        self.tFApplied3Text.move(1058,480)     

        #Creates manual input UI elements for the Grid section
        self.textGrid = QLabel("Grid Variables", self)
        self.textGrid.setFont((QFont('Arial', 12)))
        self.textGrid.move(730,580)
        self.textGrid.resize(400,40)
        self.aPointsText = QLabel("Input Angular Points: ", self)
        self.aPointsText.move(700,640)
        self.aPointsText.resize(450,40)
        self.aPointsBox = QLineEdit(self)
        self.aPointsBox.move(965,640)
        self.aPointsBox.resize(180,40)
        self.radPointsText = QLabel("Input Radial Points: ", self)
        self.radPointsText.move(700,700)
        self.radPointsText.resize(450,40)
        self.radPointsBox = QLineEdit(self)
        self.radPointsBox.move(960,700)
        self.radPointsBox.resize(180,40)
        self.radSubText = QLabel("Input Radial Substeps: ", self)
        self.radSubText.move(700,760)
        self.radSubText.resize(450,40)
        self.radSubBox = QLineEdit(self)
        self.radSubBox.move(980,760)
        self.radSubBox.resize(180,40)

        #Creates other UI elements such as certain check boxes/text and other UI stuff
        self.keepFile = QCheckBox("", self)
        self.keepFile.setChecked(False)
        self.keepFile.move(800,960)
        self.keepFile.resize(400,40)
        self.keepFileBox = QLabel("*Keep Created .yaml File", self)
        self.keepFileBox.move(838,960)
        self.keepFileBox.resize(300,40)
        self.runProgramButton = QPushButton('Run Program', self)
        self.runProgramButton.move(1350,1020)
        self.runProgramButton.resize(400,40)
        self.runProgramButton.clicked.connect(self.runProg)
        self.file = QPushButton('*.yaml File Upload', self)
        self.file.move(1350,160)
        self.file.resize(400,40)
        self.file.clicked.connect(self.fileInp)
        self.more = QPushButton('*More Information', self)
        self.more.move(1350,960)
        self.more.resize(400,40)
        self.more.clicked.connect(self.moreInfo)
        self.fileOut = QListWidget(self) #Creates a widget to display the download path for yaml upload
        self.fileOut.setGeometry(100,400,400,100)
        self.fileOut.setStyleSheet("border: 1px solid #fff; padding: 10px; border-style: solid; color: #EEEADE; border-radius: 10px; background: #616161;")
        self.fileOut.move(1350,220)
        self.pickleBox = QPushButton("*Pyv Coma Pickle File Upload", self)
        self.pickleBox.move(1350,380)
        self.pickleBox.resize(400,40)
        self.pickleBox.clicked.connect(self.pickleInp)
        self.pickleOut = QListWidget(self)
        self.pickleOut.setGeometry(100,400,400,100)
        self.pickleOut.move(1350,440)
        self.pickleOut.setStyleSheet("border: 1px solid #fff; padding: 10px; border-style: solid; color: #EEEADE; border-radius: 10px; background: #616161;")
        self.typeProgram = QLabel('Type of Program Input', self)
        self.typeProgram.setFont((QFont('Arial', 12)))
        self.typeProgram.move(1380,615)
        self.typeProgram.resize(350,40)
        self.manProgramButton = QRadioButton('', self)
        self.manProgramButton.move(1400,680)
        self.manProgramButton.resize(400,40)
        self.manProgramButton.setChecked(True)
        self.manProgramButtonText = QLabel('Manual Input', self)
        self.manProgramButtonText.move(1435,682)
        self.manProgramButtonText.resize(200,40)
        self.manProgramButtonText.setStyleSheet("color: #EEEADE; background: #616161")
        self.yamlProgramButton = QRadioButton('', self)
        self.yamlProgramButton.move(1400,730)
        self.yamlProgramButton.resize(400,40)
        self.yamlProgramButtonText = QLabel('File Input (.yaml)', self)
        self.yamlProgramButtonText.move(1435,732)
        self.yamlProgramButtonText.resize(250,40)
        self.yamlProgramButtonText.setStyleSheet("color: #EEEADE; background: #616161")
        self.pickleProgramButton = QRadioButton('', self)
        self.pickleProgramButton.move(1400,780)
        self.pickleProgramButton.resize(400,40)
        self.pickleProgramButtonText = QLabel('File Input (Pickle)', self)
        self.pickleProgramButtonText.resize(250,40)
        self.pickleProgramButtonText.move(1435,782)
        self.pickleProgramButtonText.setStyleSheet("color: #EEEADE; background: #616161")

        self.show() #Shows the window

    #Creates pop up windows for successful run or error throws
    def popUpWin(self, type, message=None):
        self.message = QMessageBox() #Creates the QMessageBox() object
        if(type == 'success'): #Successful run pop up
            self.message.setIcon(QMessageBox.Information) #Sets icon for the window
            self.message.setWindowTitle("Success")
            self.message.setText("Program run successful!")
        else:
            self.message.setIcon(QMessageBox.Critical)
            self.message.setWindowTitle("Error")
            if(type == 'incorrect yaml'): #Yaml file has an incorrect data type, almost always string to float/int
                self.message.setText(f"The .yaml file is either missing or has an incorrect data type assigned to: \"{message}\". Please try again.")
            elif(type == 'incorrect pickle'): #Pickle file can not be understood by pyvectorial
                self.message.setText("The pickle file could not be understood. Please try again.")
            elif(type == 'no file'): #User selected yaml or pickle file input but never gave a file
                self.message.setText("A file has not been selected. Please try again.")
            elif(type == 'incorrect data'): #User input an incorrect data type, almost always string to float/int
                 self.message.setText(f"Incorrect manual data entry for: \"{message}\". Please try again.")
            elif(type == 'too many boxes'): #User selected too many boxes for an input that only accepts 1 selected
                self.message.setText(f"Too many input boxes selected for: \"{message}\". Please try again.")
            elif(type == 'no boxes'): #User selected no boxes for an input that only accepts 1 selected
                self.message.setText(f"No input boxes selected for: \"{message}\". Please try again.")
        self.message.show() #Shows the pop up window

    #File Path References

    #Gets the name/file path of the pickle file.
    def pickleInp(self):
        self.pickleOut.clear() #Clears the output of the pickleOut widget that displays the path for the user
        UIVariables.PyvComaPickle = None #Clears any previous file path
        file = QFileDialog.getOpenFileNames(self, 'Open file')[0] #Gets the file path
        i = 0
        while i < len(file):
            self.pickleOut.addItem(file[i]) #Adds the path of the pickle file to the pickleOut widget
            UIVariables.PyvComaPickle = file[i] #Sets the file path to UIVariables
            i += 1
        return
    
    #Gets the name/file path of the yaml file.
    def fileInp(self):
        self.fileOut.clear()
        UIVariables.DownFile = None
        file = QFileDialog.getOpenFileNames(self, 'Open file', '', 'Yaml files (*.yaml)')[0] #Gets the file path, only allowing .yaml files to be selected
        i = 0
        while i < len(file):
            self.fileOut.addItem(file[i])
            UIVariables.DownFile = file[i]
            i += 1
        return

    #References the MoreWindow() above when the more infomation button is pressed.
    def moreInfo(self, checked):
        self.Win = MoreWindow()
        self.Win.show()
    
    #Refences the TineVarWindow() above when the time variation button is pressed.
    def timeVarWin(self, checked):
        self.Win = TimeVarWindow()
        self.Win.show()
        
    #Run Program button
    def runProg(self):
        UIVariables.PickleInputs = False
        UIVariables.FileName = None

        #Manual input runner
        #Test proper user input and assigns the results to global variables in UIVariables.py
        #Throws errors if user input is not correct
        if(self.manProgramButton.isChecked()):
            UIVariables.FileName = 'pyvectorial.yaml'

            #Param Declarations
            if(FileRunner.valueTest(self.baseQBox.text(), 'float')): #Test to see if the manual input is a correct type for all data required
                UIVariables.BaseQ = float(self.baseQBox.text()) #Sets the variable converted from string to float to UIVariables.py
            else:
                self.popUpWin('incorrect data', 'Base Q') #Throws an error if any data is an incorrect type and exits the program
                return

            #Parent Declarations
            UIVariables.ParentName = self.parNameBox.text()
            if(FileRunner.valueTest(self.outVBox.text(), 'float')):
                UIVariables.VOutflow = float(self.outVBox.text())
            else:
                self.popUpWin('incorrect data', 'Outflow Velocity')
                return
            if(FileRunner.valueTest(self.tauDBox.text(), 'float')):
                UIVariables.TauD = float(self.tauDBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_D')
                return
            if(FileRunner.valueTest(self.tauTParBox.text(), 'float')):
                UIVariables.TauTParent = float(self.tauTParBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_T')
                return
            if(FileRunner.valueTest(self.sigmaBox.text(), 'float')):
                UIVariables.Sigma = float(self.sigmaBox.text())
            else:
                self.popUpWin('incorrect data', 'Sigma')
                return
            if(FileRunner.valueTest(self.t_DBox.text(), 'float')):
                UIVariables.TtoDRatio = float(self.t_DBox.text())
            else:
                self.popUpWin('incorrect data', 'T to D Ratio')
                return

            #Fragment Declarations
            UIVariables.FragmentName = self.fragNameBox.text()
            if(FileRunner.valueTest(self.vPhotoBox.text(), 'float')):
                UIVariables.VPhoto = float(self.vPhotoBox.text())
            else:
                self.popUpWin('incorrect data', 'VPhoto')
                return
            if(FileRunner.valueTest(self.tauTFragBox.text(), 'float')):
                UIVariables.TauTFragment = float(self.tauTFragBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_T')
                return

            #Comet Declarations
            UIVariables.CometName = self.cometNameBox.text()
            if(FileRunner.valueTest(self.rHBox.text(), 'float')):
                UIVariables.Rh = float(self.rHBox.text())
            else:
                self.popUpWin('incorrect data', 'Rh')
                return
            UIVariables.CometDelta = self.deltaComBox.text()
            if((self.tFApplied1.isChecked() == False)
                and (self.tFApplied2.isChecked() == False)
                and (self.tFApplied3.isChecked() == False)):
                self.popUpWin('no boxes', 'Transformation Method') #Throws an error if there is no TFApplied box selected
                return
            elif((self.tFApplied1.isChecked() == True) #Checks all 3 tFApplied boxes to make sure only
                and (self.tFApplied2.isChecked() == False) #1 was selected and assigns it to the correct value
                and (self.tFApplied3.isChecked() == False)):
                UIVariables.TransformMethod = "cochran_schleicher_93"
                UIVariables.ApplyTransforMethod = True
            elif((self.tFApplied1.isChecked() == False)
                and (self.tFApplied2.isChecked() == True)
                and (self.tFApplied3.isChecked() == False)):
                UIVariables.TransformMethod = "festou_fortran"
                UIVariables.ApplyTransforMethod = True
            elif((self.tFApplied1.isChecked() == False)
                and (self.tFApplied2.isChecked() == False)
                and (self.tFApplied3.isChecked() == True)):
                UIVariables.TransformMethod = None
                UIVariables.ApplyTransforMethod = False
            else:
                self.popUpWin('too many boxes', 'Transformation Method') #Throws an error if there are more than 1 TFApplied box selected
                return

            #Grid Declarations
            if(FileRunner.valueTest(self.aPointsBox.text(), 'int')):
                UIVariables.AngularPoints = int(self.aPointsBox.text())
            else:
                self.popUpWin('incorrect data', 'Angular Points')
                return
            if(FileRunner.valueTest(self.radPointsBox.text(), 'int')):
                UIVariables.RadialPoints = int(self.radPointsBox.text())
            else:
                self.popUpWin('incorrect data', 'Radial Points')
                return
            if(FileRunner.valueTest(self.radSubBox.text(), 'int')):
                UIVariables.RadialSubsteps = int(self.radSubBox.text())
            else:
                self.popUpWin('incorrect data', 'Radial Substeps')
                return
            
            #Runs the program
            vmc, vmr = FileRunner.runManualProgram() #Runs the manuel program, creating a yaml file, vmc and vmr in FileCreator.py and FileRunner.py
            if(self.keepFile.isChecked() == False): #Removes the file if the keepFile == False
                FileCreator.removeFile('pyvectorial.yaml')
            self.popUpWin('success') #Opens the successful run pop up window
            self.Win = ResultsWindow(vmc, vmr) #Creates the results with the vmc and vmr
            self.Win.show() #Shows the results window
            return
        
        #Yaml input runner
        #Test to see if the file is properly formatted and will compute the results if so
        #Throws an error if the test fails
        elif(self.yamlProgramButton.isChecked()):
            UIVariables.FileName = UIVariables.DownFile
            if (os.path.exists(f"{UIVariables.FileName}") == False): #Test to see if the user uploaded a file
                self.popUpWin('no file')
                return
            testResult, message = FileRunner.fileTest(UIVariables.FileName) #Gets the bool test result and a message if testResult = False
            if (testResult): #Reads the file to see if it is formatted properly  
                #Runs the program
                vmc, vmr = FileRunner.runFileYamlProgram(UIVariables.FileName) #Runs the yaml file, creating a vmc and vmr in FileRunner.py
                self.popUpWin('success')
                self.Win = ResultsWindow(vmc, vmr)
                self.Win.show()
            else:
                self.popUpWin('incorrect yaml', message) #Throws an error meaning that the user's file dict was missing important info
            return
        
        #Pickle input runner
        #Test to see if the pickle file can be understood and runs the results from that.
        #Throws an error if the test fails.
        elif(self.pickleProgramButton.isChecked()):
            UIVariables.PickleInputs = True
            UIVariables.FileName = UIVariables.PyvComaPickle
            if (os.path.exists(f"{UIVariables.FileName}") == False): #Test to see if the user uploaded a file
                self.popUpWin('no file')
                return
            if(FileRunner.pickleTest(UIVariables.FileName) == False): #Test to see if pyvectorial can read the pickle in FileRunner.py
                self.popUpWin('incorrect pickle')
                return
            #Runs the program
            vmc, vmr = FileRunner.runFilePickleProgram(UIVariables.FileName) #Runs the pickle file, creating a default vmc and proper vmr in FileRunner.py
            self.popUpWin('success')
            self.Win = ResultsWindow(vmc, vmr) 
            self.Win.show() 
            return

#Defines the UI when initially running the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #Defines the style format for the whole app/main window (for aesthetic purposes only)
    #Other windows or Q objects can override this style by declaring a new setStyleSheet()
    app.setStyleSheet("""
    QMainWindow{ 
        background-color: #1F2022; 
    }
    QListWidget {
        border: 2px solid #fff;
        padding: 10px;
        border-style: solid;
        border-radius: 10px;
        background: #3D3D3D; 
    }
    QLabel {
        color: #EEEADE;
        background: #3D3D3D;
    }
    QLineEdit {
        padding: 1px;
        color: #EEEADE;
        border-style: solid;
        border: 1px solid #EEEADE;
        border-radius: 8px;
        background: #616161
    }
    QPushButton {
        padding: 1px;
        color: #EEEADE;
        border-style: solid;
        border: 1px solid #EEEADE;
        border-radius: 8px;
        background: #616161
    }
    QPushButton:hover {
        border: 1px #C6C6C6 solid;
        color: #fff;
        background: #0892D0;
    }
    QFileDialog {
        background: #616161;
        color: #3D3D3D;
    }
    QMessageBox {
        background: #3D3D3D
    }    """)
    Win = App() #Only shows App() on start up
    Win.show()
    sys.exit(app.exec_())