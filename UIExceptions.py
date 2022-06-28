#Program to raise exceptions based on user data in UIReader.py.
#Creates a pop up message that describes the exception that is raised by using PyQt5.
#
#Author: Jacob Duffy
#Version: 6/28/2022

#Exception where user puts an incorrect data type in a text box 
#(ie: String input when a float was required).
class invalidUserInput(Exception):
    def __init__():
        return 0

#Exception where a user does not fill all text boxes or 
#leaves an important check box unchecked.
class missingUserInput(Exception):
    def __init__():
        return 0