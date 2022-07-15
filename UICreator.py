#Driver program to create a UI to read in vectorial model data for comet analysis
#and create multiple results graphs using MatPlotLib.
#Uses PyQt5 as the interface to create the UI.
#This work is based on a pvvectorial repository created by sjoset.
#
#Author: Jacob Duffy
#Version: 7/14/2022

import UIVariables
import FileRunner
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QListWidget, QTabWidget
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QLabel, QCheckBox, QFileDialog, QVBoxLayout
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
        self.RadDensityResults = QLabel(f"{FileRunner.getPrintRadialDensity(self.vmr)}", self)
        self.RadDensityResults.move(0,0)
        self.ColumnDensityResults = QLabel(f"{FileRunner.getPrintColumnDensity(self.vmr)}", self)
        self.ColumnDensityResults.move(600,30)
        self.AgreementCheckResults = QLabel(f"{FileRunner.getAgreementCheck(self.vmr)}", self)
        self.AgreementCheckResults.move(1200,30)

        #Test to see if pickle input was used as UIVariables.ApertureChecks == None if it was as
        #no coma object was created
        if (UIVariables.PickleInputs == False):
            self.AgreementCheckResults = QLabel(f"{UIVariables.ApertureChecks}", self)
            self.AgreementCheckResults.move(1200,200)

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
        self.layout = QVBoxLayout() #Defines the full window layout
        self.tabs = QTabWidget() #Creates a widget containing the tabs
        self.FragSput = QWidget() #Creates a bunch of empty widgets used in each tab
        self.Radial = QWidget()
        self.ColumD = QWidget()
        self.ColumD3 = QWidget()
        self.ColumD3C = QWidget()

        #Plots and displays the fragment sputter graph
        self.tabs.addTab(self.FragSput, "Fragment Sputter") #Creates the tab named "Fragment Sputter"
        self.FragSput.layout = QVBoxLayout(self) #Defines the tab layout as "QVBoxLayout"
        self.FragSputGraph = PlotGraphs(self.vmc, self.vmr, "frag sput", width=5, height=4, dpi=100) #Creates the graph
        self.FragSputToolbar = NavigationToolbar2QT(self.FragSputGraph, self) #Creates the toolbar for the graph
        self.FragSput.layout.addWidget(self.FragSputGraph) #Adds the graph to the QVBoxLayout
        self.FragSput.layout.addWidget(self.FragSputToolbar) #Adds the toolbar to the QVBoxLayout
        self.FragSput.setLayout(self.FragSput.layout) #Finalizes the tab layout
        
        #Plots and displays the radial plot graph
        self.tabs.addTab(self.Radial, "Radial")
        self.Radial.layout = QVBoxLayout(self)
        self.RadialGraph = PlotGraphs(self.vmc, self.vmr, "radial", width=5, height=4, dpi=100)
        self.RadialToolbar = NavigationToolbar2QT(self.RadialGraph, self)
        self.Radial.layout.addWidget(self.RadialGraph)
        self.Radial.layout.addWidget(self.RadialToolbar)
        self.Radial.setLayout(self.Radial.layout)
        
        #Plots and displays the column density graph
        self.tabs.addTab(self.ColumD, "Column Density")
        self.ColumD.layout = QVBoxLayout(self)
        self.ColumDGraph = PlotGraphs(self.vmc, self.vmr, "column dens", width=5, height=4, dpi=100)
        self.ColumDToolbar = NavigationToolbar2QT(self.ColumDGraph, self)
        self.ColumD.layout.addWidget(self.ColumDGraph)
        self.ColumD.layout.addWidget(self.ColumDToolbar)
        self.ColumD.setLayout(self.ColumD.layout)
        
        #Plots and displays the column density graph (off centered)
        self.tabs.addTab(self.ColumD3, "Column Density (3D Off Centered)")
        self.ColumD3.layout = QVBoxLayout(self)
        self.ColumD3Graph = PlotGraphs(self.vmc, self.vmr, "3d column dens", width=5, height=4, dpi=100)
        self.ColumD3Toolbar = NavigationToolbar2QT(self.ColumD3Graph, self)
        self.ColumD3.layout.addWidget(self.ColumD3Graph)
        self.ColumD3.layout.addWidget(self.ColumD3Toolbar)
        self.ColumD3.setLayout(self.ColumD3.layout)
        
        #Plots and displays the column density graph (centered)
        self.tabs.addTab(self.ColumD3C, "Column Density (3D Centered)")
        self.ColumD3C.layout = QVBoxLayout(self)
        self.ColumD3CGraph = PlotGraphs(self.vmc, self.vmr, "3d column dens cent", width=5, height=4, dpi=100)
        self.ColumD3CToolbar = NavigationToolbar2QT(self.ColumD3CGraph, self)
        self.ColumD3C.layout.addWidget(self.ColumD3CGraph)
        self.ColumD3C.layout.addWidget(self.ColumD3CToolbar)
        self.ColumD3C.setLayout(self.ColumD3C.layout)
    
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
        self.width = 1400
        self.height = 900
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label1 = QLabel("Sine", self)
        self.label1.setFont((QFont('Arial', 18)))
        self.label1.move(150,20)
        self.label2 = QLabel("Gaussian", self)
        self.label2.setFont((QFont('Arial', 18)))
        self.label2.move(900,20)
        self.label3 = QLabel("Square", self)
        self.label3.setFont((QFont('Arial', 18)))
        self.label3.move(150,500)
        self.TVSineBox = QCheckBox("*Select Sine Time Variation", self)
        self.TVSineBox.setChecked(False)
        self.TVSineBox.move(20,100)
        self.TVSineBox.resize(500,40)
        self.TVGausBox = QCheckBox("*Select Gaussian Time Variation", self)
        self.TVGausBox.setChecked(False)
        self.TVGausBox.move(800,100)
        self.TVGausBox.resize(500,40)
        self.TVSquareBox = QCheckBox("*Select Square Pulse Time Variation", self)
        self.TVSquareBox.setChecked(False)
        self.TVSquareBox.move(20,580)
        self.TVSquareBox.resize(500,40)
        self.NoTVBox = QCheckBox("*Select For No Time Variation", self)
        self.NoTVBox.setChecked(True)
        self.NoTVBox.move(800,580)
        self.NoTVBox.resize(500,40)

        #Creates UI elements for sine input
        self.SineAmpText = QLabel("Input Amplitude: ", self)
        self.SineAmpText.move(20,180)
        self.SineAmpText.resize(300,40)
        self.SineAmpBox = QLineEdit(self)
        self.SineAmpBox.move(240,180)
        self.SineAmpBox.resize(180,40)
        self.SineAmpUnits = QLabel("molecules/sec", self)
        self.SineAmpUnits.move(430,180)
        self.SineAmpUnits.resize(300,40)
        self.SinePeriodText = QLabel("Input Period: ", self)
        self.SinePeriodText.move(20,240)
        self.SinePeriodText.resize(300,40)
        self.SinePeriodBox = QLineEdit(self)
        self.SinePeriodBox.move(200,240)
        self.SinePeriodBox.resize(180,40)
        self.SinePeriodUnits = QLabel("hours", self)
        self.SinePeriodUnits.move(390,240)
        self.SinePeriodUnits.resize(300,40)
        self.SineDeltaText = QLabel("Input Delta: ", self)
        self.SineDeltaText.move(20,300)
        self.SineDeltaText.resize(300,40)
        self.SineDeltaBox = QLineEdit(self)
        self.SineDeltaBox.move(190,300)
        self.SineDeltaBox.resize(180,40)
        self.SineDeltaUnits = QLabel("angular offset in hours", self)
        self.SineDeltaUnits.move(380,300)
        self.SineDeltaUnits.resize(300,40)

        #Creates UI elements for gaussian input
        self.GausAmpText = QLabel("Input Amplitude: ", self)
        self.GausAmpText.move(800,180)
        self.GausAmpText.resize(300,40)
        self.GausAmpBox = QLineEdit(self)
        self.GausAmpBox.move(1020,180)
        self.GausAmpBox.resize(180,40)
        self.GausAmpUnits = QLabel("molecules/sec", self)
        self.GausAmpUnits.move(1210,180)
        self.GausAmpUnits.resize(300,40)
        self.GausStdText = QLabel("Input Standard Deviation: ", self)
        self.GausStdText.move(800,240)
        self.GausStdText.resize(350,40)
        self.GausStdBox = QLineEdit(self)
        self.GausStdBox.move(1120,240)
        self.GausStdBox.resize(180,40)
        self.GausStdUnits = QLabel("hours", self)
        self.GausStdUnits.move(1310,240)
        self.GausStdUnits.resize(300,40)
        self.GausTPText = QLabel("Input Time at Peak: ", self)
        self.GausTPText.move(800,300)
        self.GausTPText.resize(350,40)
        self.GausTPBox = QLineEdit(self)
        self.GausTPBox.move(1045,300)
        self.GausTPBox.resize(180,40)
        self.GausTPUnits = QLabel("hours", self)
        self.GausTPUnits.move(1235,300)
        self.GausTPUnits.resize(300,40)

        #Creates UI elements for square input
        self.SquareAmpText = QLabel("Input Amplitude: ", self)
        self.SquareAmpText.move(20,640)
        self.SquareAmpText.resize(300,40)
        self.SquareAmpBox = QLineEdit(self)
        self.SquareAmpBox.move(240,640)
        self.SquareAmpBox.resize(180,40)
        self.SquareAmpUnits = QLabel("molecules/sec", self)
        self.SquareAmpUnits.move(430,640)
        self.SquareAmpUnits.resize(300,40)
        self.SquareDurText = QLabel("Input Duration: ", self)
        self.SquareDurText.move(20,700)
        self.SquareDurText.resize(300,40)
        self.SquareDurBox = QLineEdit(self)
        self.SquareDurBox.move(230,700)
        self.SquareDurBox.resize(180,40)
        self.SquareDurUnits = QLabel("hours", self)
        self.SquareDurUnits.move(420,700)
        self.SquareDurUnits.resize(300,40)
        self.SquareTSPText = QLabel("Input Start of Pulse: ", self)
        self.SquareTSPText.move(20,760)
        self.SquareTSPText.resize(300,40)
        self.SquareTSPBox = QLineEdit(self)
        self.SquareTSPBox.move(280,760)
        self.SquareTSPBox.resize(180,40)
        self.SquareTSPUnits = QLabel("hours", self)
        self.SquareTSPUnits.move(470,760)
        self.SquareTSPUnits.resize(300,40)

        self.button = QPushButton('Set Time Variation Method', self)
        self.button.move(800,820)
        self.button.resize(400,40)
        self.button.clicked.connect(self.setResults)

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
            if(type == 'no input'): #User did not select any of the 4 time variation type boxes
                self.message.setText("No time variation type selected. Please try again.")
            elif(type == 'incorrect data'):
                 self.message.setText(f"Incorrect manual data entry for: \"{message}\". Please try again.")
            elif(type == 'too many boxes'): #User selected too many of the time variation type boxes
                self.message.setText(f"Too many time variation boxes selected. Please try again.")
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

        #Throws an error if no time varaition types are selected
        if((self.TVSineBox.isChecked() == False) and 
            (self.TVGausBox.isChecked() == False) and
            (self.TVSquareBox.isChecked() == False) and
            (self.NoTVBox.isChecked() == False)):
            self.popUpWin('no input')
            return
        
        #Declarations if sine time variation is selected
        if((self.TVSineBox.isChecked() == True) and 
            (self.TVGausBox.isChecked() == False) and
            (self.TVSquareBox.isChecked() == False) and
            (self.NoTVBox.isChecked() == False)):
            UIVariables.TimeVariationType = 'sine wave'
            if(FileRunner.valueTest(self.SineAmpBox.text(), 'float')):
                UIVariables.SinAmp = float(self.SineAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.SinePeriodBox.text(), 'float')):
                UIVariables.SinPer = float(self.SinePeriodBox.text())
            else:
                self.popUpWin('incorrect data', 'Period')
                return
            if(FileRunner.valueTest(self.SineDeltaBox.text(), 'float')):
                UIVariables.SinDelta = float(self.SineDeltaBox.text())
            else:
                self.popUpWin('incorrect data', 'Delta')
                return
            self.popUpWin('success', 'Sine')
            return

        #Declarations if gaussian time variation is selected
        elif((self.TVSineBox.isChecked() == False) and 
            (self.TVGausBox.isChecked() == True) and
            (self.TVSquareBox.isChecked() == False) and
            (self.NoTVBox.isChecked() == False)):
            UIVariables.TimeVariationType = 'gaussian'
            if(FileRunner.valueTest(self.GausAmpBox.text(), 'float')):
                UIVariables.GausAmp = float(self.GausAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.GausStdBox.text(), 'float')):
                UIVariables.GausSTD = float(self.GausStdBox.text())
            else:
                self.popUpWin('incorrect data', 'Standard Deviation')
                return
            if(FileRunner.valueTest(self.GausTPBox.text(), 'float')):
                UIVariables.GausT_Max = float(self.GausTPBox.text())
            else:
                self.popUpWin('incorrect data', 'Time at Peak')
                return
            self.popUpWin('success', 'Gaussian')
            return

        #Declarations if square time variation is selected
        elif((self.TVSineBox.isChecked() == False) and 
            (self.TVGausBox.isChecked() == False) and
            (self.TVSquareBox.isChecked() == True) and
            (self.NoTVBox.isChecked() == False)):
            UIVariables.TimeVariationType = 'square pulse'
            if(FileRunner.valueTest(self.SquareAmpBox.text(), 'float')):
                UIVariables.SquareAmp = float(self.SquareAmpBox.text())
            else:
                self.popUpWin('incorrect data', 'Amplitude')
                return
            if(FileRunner.valueTest(self.SquareDurBox.text(), 'float')):
                UIVariables.SquareDur = float(self.SquareDurBox.text())
            else:
                self.popUpWin('incorrect data', 'Duration')
                return
            if(FileRunner.valueTest(self.SquareTSPBox.text(), 'float')):
                UIVariables.SquareT_Start = float(self.SquareTSPBox.text())
            else:
                self.popUpWin('incorrect data', 'Start of Pulse')
                return
            self.popUpWin('success', 'Square')
            return
        
        #Declarations if no time variation is selected
        elif((self.TVSineBox.isChecked() == False) and 
            (self.TVGausBox.isChecked() == False) and
            (self.TVSquareBox.isChecked() == False) and
            (self.NoTVBox.isChecked() == True)):
            self.popUpWin('success', 'None')
            return
        
        #Throws an error if are too many time varaition types are selected
        else:
            self.popUpWin('too many boxes')
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
        self.height = 1050
        self.initUI()

    #Defines the UI Interface
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Input text
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
        self.inputText7 = QLabel("---A .yaml file will only be understood if it is formatted the proper way.", self)
        self.inputText7.move(20,410)
        self.inputText8 = QLabel("(look at a manually created .yaml file for this format).", self)
        self.inputText8.move(20,440)
        self.inputText9 = QLabel("---The \"Pvy coma pickle\" is a special file that will not create a vmc", self)
        self.inputText9.move(20,490)
        self.inputText10 = QLabel("when running the program.", self)
        self.inputText10.move(20,520)

        #Output text
        self.label1 = QLabel("Outputs", self)
        self.label1.setFont((QFont('Arial', 18)))
        self.label1.move(450,600)
        self.outputText1 = QLabel ("---When finished the program will give the user:", self)
        self.outputText1.move(20,680)
        self.outputText2 = QLabel ("Fragment Sputter Graph", self)
        self.outputText2.move(150,720)
        self.outputText3 = QLabel ("Radial Density Graph", self)
        self.outputText3.move(150,760)
        self.outputText4 = QLabel ("Column Density Graphs (2D, 3D centered, 3D off centered)", self)
        self.outputText4.move(150,800)
        self.outputText5 = QLabel ("Radius vs. Fragment Densitiy Table", self)
        self.outputText5.move(150,840)
        self.outputText6 = QLabel ("Radius vs. Column Densitiy Table", self)
        self.outputText6.move(150,880)
        self.outputText7 = QLabel ("Fragment Agreement Check", self)
        self.outputText7.move(150,920)
        self.outputText8 = QLabel ("Fragment Aperture Check (not given for pickle file input)", self)
        self.outputText8.move(150,960)
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
        self.height = 1400 #Defines the size of the UI window
        self.initUI()
    
    #Defines the UI Interface
    def initUI(self):

        #UI Element creator
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Creates title headers for the UI
        self.box1 = QLabel("Manual Inputs", self) #Creates a text box with the input string
        self.box1.move(570,10) #Moves variable text to the (x,y) on the UI window
        self.box1.setFont((QFont('Arial', 18))) #Sets font to the input string and font size
        self.box1.resize(550,60) #Resize the text to fill up the (x,y)
        self.box2 = QLabel("File Inputs", self)
        self.box2.move(1020,950)
        self.box2.setFont((QFont('Arial', 18)))
        self.box2.resize(550,60)
        
        #Creates manual input UI elements for the Production section
        self.textPro = QLabel("Production Variables", self)
        self.textPro.setFont((QFont('Arial', 12)))
        self.textPro.move(50,160)
        self.textPro.resize(400,40)
        self.BaseQText = QLabel("Input Base Q: ", self)
        self.BaseQText.move(20,220)
        self.BaseQText.resize(180,40)
        self.BaseQBox = QLineEdit(self) #Creates a textbox for user to input data in
        self.BaseQBox.move(200,220)
        self.BaseQBox.resize(180,40)
        self.BaseQUnits = QLabel("prod/sec", self)
        self.BaseQUnits.move(400,220)
        self.BaseQUnits.resize(180,40)
        self.TimeVarBox = QPushButton("*Select Time Variation Method", self)
        self.TimeVarBox.move(20,280)
        self.TimeVarBox.resize(400,40)
        self.TimeVarBox.clicked.connect(self.timeVarWin) #Defines the method call when the button is clicked

        #Creates manual input UI elements for the Parent section
        self.textPar = QLabel("Parent Variables", self)
        self.textPar.setFont((QFont('Arial', 12)))
        self.textPar.move(50,380)
        self.textPar.resize(400,40)
        self.ParNameText = QLabel("*Input Parent Name: ", self)
        self.ParNameText.move(20,440)
        self.ParNameText.resize(300,40)
        self.ParNameBox = QLineEdit(self)
        self.ParNameBox.move(270,440)
        self.ParNameBox.resize(180,40)
        self.OutVText = QLabel("Input Outflow Velocity: ", self)
        self.OutVText.move(20,500)
        self.OutVText.resize(300,40)
        self.OutVBox = QLineEdit(self)
        self.OutVBox.move(300,500)
        self.OutVBox.resize(180,40)
        self.OutVUnits = QLabel("km/hour", self)
        self.OutVUnits.move(500,500)
        self.OutVUnits.resize(300,40)
        self.TauDText = QLabel("Input Tau_D: ", self)
        self.TauDText.move(20,560)
        self.TauDText.resize(300,40)
        self.TauDBox = QLineEdit(self)
        self.TauDBox.move(185,560)
        self.TauDBox.resize(180,40)
        self.TauDUnits = QLabel("sec", self)
        self.TauDUnits.move(385,560)
        self.TauDUnits.resize(300,40)
        self.TauTParText = QLabel("Input Tau_T: ", self)
        self.TauTParText.move(20,620)
        self.TauTParText.resize(300,40)
        self.TauTParUnits = QLabel("sec", self)
        self.TauTParUnits.move(385,620)
        self.TauTParUnits.resize(300,40)
        self.TauTParBox = QLineEdit(self)
        self.TauTParBox.move(185,620)
        self.TauTParBox.resize(180,40)
        self.SigmaText = QLabel("Input Sigma: ", self)
        self.SigmaText.move(20,680)
        self.SigmaText.resize(300,40)
        self.SigmaBox = QLineEdit(self)
        self.SigmaBox.move(185,680)
        self.SigmaBox.resize(180,40)
        self.SigmaUnits = QLabel("cm^2", self)
        self.SigmaUnits.move(385,680)
        self.SigmaUnits.resize(300,40)
        self.T_DText = QLabel("Input T to D Ratio: ", self)
        self.T_DText.move(20,740)
        self.T_DText.resize(300,40)
        self.T_DBox = QLineEdit(self)
        self.T_DBox.move(250,740)
        self.T_DBox.resize(180,40) 

        #Creates manual input UI elements for the Fragment section  
        self.textFrag = QLabel("Fragment Variables", self)
        self.textFrag.setFont((QFont('Arial', 12)))
        self.textFrag.move(50,840)
        self.textFrag.resize(400,40) 
        self.FragNameText = QLabel("*Input Fragment Name: ", self)
        self.FragNameText.move(20,900)
        self.FragNameText.resize(300,40)
        self.FragNameBox = QLineEdit(self)
        self.FragNameBox.move(310,900)
        self.FragNameBox.resize(180,40)  
        self.VPhotoText = QLabel("Input VPhoto: ", self)
        self.VPhotoText.move(20,960)
        self.VPhotoText.resize(300,40)
        self.VPhotoBox = QLineEdit(self)
        self.VPhotoBox.move(190,960)
        self.VPhotoBox.resize(180,40)
        self.VPhotoUnits = QLabel("km/hour", self)
        self.VPhotoUnits.move(390,960)
        self.VPhotoUnits.resize(300,40)
        self.TauTFragText = QLabel("Input Tau_T: ", self)
        self.TauTFragText.move(20,1020)
        self.TauTFragText.resize(300,40)
        self.TauTFragBox = QLineEdit(self)
        self.TauTFragBox.move(185,1020)
        self.TauTFragBox.resize(180,40)    
        self.TauTFragUnits = QLabel("sec", self)
        self.TauTFragUnits.move(385,1020)
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
        self.DeltaComBox.move(1020,340)
        self.DeltaComBox.resize(180,40)
        self.TFMethText = QLabel("*Transformation Method: ", self)
        self.TFMethText.move(850,400)
        self.TFMethText.resize(450,40)
        self.TFApplied1 = QCheckBox("Cochran", self) #Set checkable box
        self.TFApplied1.setChecked(False) #Set checked box to be unchecked when the window is created
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

        #Creates other UI elements such as certain check boxes/text and other UI stuff
        self.KeepFile = QCheckBox("*Keep Created .yaml File", self)
        self.KeepFile.setChecked(False)
        self.KeepFile.move(850,780)
        self.KeepFile.resize(500,40)
        self.FileInputBox = QCheckBox("*Select for .yaml file input", self)
        self.FileInputBox.setChecked(False)
        self.FileInputBox.move(720,1040)
        self.FileInputBox.resize(500,40)
        self.PickleInputBox = QCheckBox("*Select for pickle file input", self)
        self.PickleInputBox.setChecked(False)
        self.PickleInputBox.move(1170,1040)
        self.PickleInputBox.resize(500,40)
        self.ManInputBox = QCheckBox("*Select for Manual Inputs", self)
        self.ManInputBox.setChecked(False)
        self.ManInputBox.move(540,100)
        self.ManInputBox.resize(500,40)
        self.button = QPushButton('Run Program', self)
        self.button.move(1350,1320)
        self.button.resize(400,40)
        self.button.clicked.connect(self.runProg)
        self.file = QPushButton('.Yaml File Upload', self)
        self.file.move(720,1100)
        self.file.resize(400,40)
        self.file.clicked.connect(self.fileInp)
        self.more = QPushButton('*More Information', self)
        self.more.move(20,1320)
        self.more.resize(400,40)
        self.more.clicked.connect(self.moreInfo)
        self.fileOut = QListWidget(self) #Creates a widget to display the download path for yaml upload
        self.fileOut.setGeometry(60,400,400,60) #Sets the geometry for the QListWidget
        self.fileOut.move(720,1160)
        self.PickleBox = QPushButton("Pyv Coma Pickle File Upload", self)
        self.PickleBox.move(1170,1100)
        self.PickleBox.resize(400,40)
        self.PickleBox.clicked.connect(self.pickleInp)
        self.pickleOut = QListWidget(self)
        self.pickleOut.setGeometry(60,400,400,60)
        self.pickleOut.move(1170,1160)

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
            if(type == 'no input'): #No input given (manual, yaml, or pickle)
                self.message.setText("No input type selected. Please try again.")
            elif(type == 'too many input'): #Too many inputs given
                self.message.setText("Too many input method types selected (manual, yaml, pickle). Please try again.")
            elif(type == 'incorrect yaml'): #Yaml file has an incorrect data type, almost always string to float/int
                self.message.setText("The .yaml file has an incorrect data entry. Please try again.")
            elif(type == 'incorrect pickle'): #Pickle file can not be understood by pyvectorial
                self.message.setText("The pickle file could not be understood. Please try again.")
            elif(type == 'no file'): #User selected yaml or pickle file input but never gave a file
                self.message.setText("A file has not been selected. Please try again.")
            elif(type == 'incorrect data'): #User input an incorrect data type, almost always string to float/int
                 self.message.setText(f"Incorrect manual data entry for: \"{message}\". Please try again.")
            elif(type == 'too many boxes'): #User selected too many boxes for a input that only accepts 1 selected
                self.message.setText(f"Too many input boxes selected for: \"{message}\". Please try again.")
            elif(type == 'no boxes'): #User selected no boxes for a input that only accepts 1 selected
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
        UIVariables.ManInputs = False
        UIVariables.FileInputs = False
        UIVariables.PickleInputs = False
        UIVariables.FileName = None

        #Throws an exception if there is no input type selected
        if((self.ManInputBox.isChecked() == False) and
            (self.FileInputBox.isChecked() == False) and
            (self.PickleInputBox.isChecked() == False)):
            self.popUpWin('no input')
            return

        #Manual input runner
        #Test proper user input and assigns the results to global variables in UIVariables.py
        #Throws errors if user input is not correct
        if(self.ManInputBox.isChecked()):
            UIVariables.ManInputs = True
            UIVariables.FileName = 'pyvectorial.yaml'

            #Param Declarations
            if(FileRunner.valueTest(self.BaseQBox.text(), 'float')): #Test to see if the manual input is a correct type for all data required
                UIVariables.BaseQ = float(self.BaseQBox.text()) #Sets the variable converted from string to float to UIVariables.py
            else:
                self.popUpWin('incorrect data', 'Base Q') #Throws an error if any data is an incorrect type and exits the program
                return

            #Parent Declarations
            UIVariables.ParentName = self.ParNameBox.text()
            if(FileRunner.valueTest(self.OutVBox.text(), 'float')):
                UIVariables.VOutflow = float(self.OutVBox.text())
            else:
                self.popUpWin('incorrect data', 'Outflow Velocity')
                return
            if(FileRunner.valueTest(self.TauDBox.text(), 'float')):
                UIVariables.TauD = float(self.TauDBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_D')
                return
            if(FileRunner.valueTest(self.TauTParBox.text(), 'float')):
                UIVariables.TauTParent = float(self.TauTParBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_T')
                return
            if(FileRunner.valueTest(self.SigmaBox.text(), 'float')):
                UIVariables.Sigma = float(self.SigmaBox.text())
            else:
                self.popUpWin('incorrect data', 'Sigma')
                return
            if(FileRunner.valueTest(self.T_DBox.text(), 'float')):
                UIVariables.TtoDRatio = float(self.T_DBox.text())
            else:
                self.popUpWin('incorrect data', 'T to D Ratio')
                return

            #Fragment Declarations
            UIVariables.FragmentName = self.FragNameBox.text()
            if(FileRunner.valueTest(self.VPhotoBox.text(), 'float')):
                UIVariables.VPhoto = float(self.VPhotoBox.text())
            else:
                self.popUpWin('incorrect data', 'VPhoto')
                return
            if(FileRunner.valueTest(self.TauTFragBox.text(), 'float')):
                UIVariables.TauTFragment = float(self.TauTFragBox.text())
            else:
                self.popUpWin('incorrect data', 'Tau_T')
                return

            #Comet Declarations
            UIVariables.CometName = self.CometNameBox.text()
            if(FileRunner.valueTest(self.RHBox.text(), 'float')):
                UIVariables.Rh = float(self.RHBox.text())
            else:
                self.popUpWin('incorrect data', 'Rh')
                return
            UIVariables.CometDelta = self.DeltaComBox.text()
            if((self.TFApplied1.isChecked() == False)
                and (self.TFApplied2.isChecked() == False)
                and (self.TFApplied3.isChecked() == False)):
                self.popUpWin('no boxes', 'Transformation Method') #Throws an error if there is no TFApplied box selected
                return
            elif((self.TFApplied1.isChecked() == True) #Checks all 3 TFApplied boxes to make sure only
                and (self.TFApplied2.isChecked() == False) #1 was selected and assigns it to the correct value
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
                self.popUpWin('too many boxes', 'Transformation Method') #Throws an error if there are more than 1 TFApplied box selected
                return

            #Grid Declarations
            if(FileRunner.valueTest(self.APointsBox.text(), 'int')):
                UIVariables.AngularPoints = int(self.APointsBox.text())
            else:
                self.popUpWin('incorrect data', 'Angular Points')
                return
            if(FileRunner.valueTest(self.RadPointsBox.text(), 'int')):
                UIVariables.RadialPoints = int(self.RadPointsBox.text())
            else:
                self.popUpWin('incorrect data', 'Radial Points')
                return
            if(FileRunner.valueTest(self.RadSubBox.text(), 'int')):
                UIVariables.RadialSubsteps = int(self.RadSubBox.text())
            else:
                self.popUpWin('incorrect data', 'Radial Substeps')
                return
            
            #Runs the program
            vmc, vmr = FileRunner.runManualProgram() #Runs the manuel program, creating a yaml file, vmc and vmr in FileCreator.py and FileRunner.py
            self.popUpWin('success') #Opens the successful run pop up window
            self.Win = ResultsWindow(vmc, vmr) #Creates the results with the vmc and vmr
            self.Win.show() #Shows the results window
            return
        
        #Yaml input runner
        #Test to see if the file is properly formatted and will compute the results if so
        #Throws an error if the test fails
        elif(self.FileInputBox.isChecked()):
            UIVariables.FileInputs = True
            UIVariables.FileName = UIVariables.DownFile
            if (os.path.exists(f"{UIVariables.FileName}") == False): #Test to see if the user uploaded a file
                self.popUpWin('no file')
                return      
            if (FileRunner.fileTest()): #Reads the file to see if it is formatted properly  
                #Runs the program
                vmc, vmr = FileRunner.runFileYamlProgram() #Runs the yaml file, creating a vmc and vmr in FileRunner.py
                self.popUpWin('success')
                self.Win = ResultsWindow(vmc, vmr)
                self.Win.show()
            else:
                self.popUpWin('incorrect yaml') #Throws an error meaning that the user's file dict was missing important info
            return
        
        #Pickle input runner
        #Test to see if the pickle file can be understood and runs the results from that.
        #Throws an error if the test fails.
        elif(self.PickleInputBox.isChecked()):
            UIVariables.PickleInputs = True
            UIVariables.FileName = UIVariables.PyvComaPickle
            if (os.path.exists(f"{UIVariables.FileName}") == False): #Test to see if the user uploaded a file
                self.popUpWin('no file')
                return
            if(FileRunner.pickleTest() == False): #Test to see if pyvectorial can read the pickle in FileRunner.py
                self.popUpWin('incorrect pickle')
                return
            #Runs the program
            vmc, vmr = FileRunner.runFilePickleProgram() #Runs the pickle file, creating a default vmc and proper vmr in FileRunner.py
            self.popUpWin('success')
            self.Win = ResultsWindow(vmc, vmr) 
            self.Win.show() 
            return

        #Throws an error if too many input boxes were selected
        else:
            self.popUpWin('too many input')
            return

#Defines the UI when initially running the program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = App() #Only shows App() on start up
    Win.show()
    sys.exit(app.exec_())