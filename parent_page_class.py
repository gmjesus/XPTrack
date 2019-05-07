import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMainWindow, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from datetime import datetime

#---------------------------------------------------
# Classes
#---------------------------------------------------

class Page(QMainWindow):
    '''Parent class of all pages.'''

    def __init__(self):
        # Constructor
        super().__init__()
   
    def defaultWindow(self,pageName):
        # Default settings for each page
        self.setWindowTitle(pageName)
        self.setStyleSheet("background-color: lightskyblue")
        self.resize(1000,900)

    def defaultButton(self,msg,x,y,fontsize,tooltip,w,h):
        # Display a button
        pushButton = QPushButton(msg,self)
        pushButton.move(x,y)
        pushButton.setStyleSheet("background-color: white; font-size: "+str(fontsize)+"px")
        pushButton.setToolTip("<h4>"+tooltip+"</h4>")
        pushButton.resize(w,h) 
        return pushButton

    def defaultLabel(self,msg,x,y):
        label = QLabel(msg, self)
        label.setFixedWidth(1000)
        label.move(x,y)
        return label
 
    def backButton(self):
        # Button to navigate to your last page
        pushButton = QPushButton("Back",self)
        pushButton.move(0,0)
        pushButton.setStyleSheet("background-color: white")
        pushButton.setToolTip("<h4>Click to go back</h4>")
        pushButton.clicked.connect(self.lastWindow)
 
    def errorMessage(self,msg):
        # Display error message
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText("Error:")
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.exec_()
