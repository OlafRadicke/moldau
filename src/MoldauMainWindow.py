#!/usr/bin/python
# -*- coding: utf-8 -*-


 ###########################################################################
 #   Copyright (C) 2010 by ATIX AG                                         #
 #                                                                         #
 #   This program is free software; you can redistribute it and/or modify  #
 #   it under the terms of the GNU General Public License as published by  #
 #   the Free Software Foundation; either version 3 of the License, or     #
 #   any later version.                                                    #
 #                                                                         #
 #   This program is distributed in the hope that it will be useful,       #
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
 #   GNU General Public License for more details.                          #
 #                                                                         #
 #   You should have received a copy of the GNU General Public License     #
 #   along with this program; if not, see                                  #
 #   http:#www.gnu.org/licenses/gpl.txt                                    #
 #                                                                         #
 #   Olaf Radicke <radicke@atix.de>                                        #
 ###########################################################################

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from MoldauConf import MoldauConf
from TasksSettings import TasksSettings




## The main window of the GUI
class MoldauMainWindow(QtGui.QMainWindow):


    ## configuraton of this applikation.
    moldauConf   = MoldauConf()
    ## The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## Constructor
    def __init__(self, *args): 
        QtGui.QWidget.__init__(self, *args) 

        self.setMinimumSize(800,680)

        #---------- menubar --------------------
        ## Menue-item for apliction exit
        menuExit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        menuExit.setShortcut('Ctrl+Q')
        menuExit.setStatusTip('Exit application')
        self.connect(menuExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))


        ## Menue-item for change the task stetting file.
        menuTasksSetting = QtGui.QAction( 'Open task seting', self)
        menuTasksSetting.setShortcut('Ctrl+T')
        menuTasksSetting.setStatusTip('Open task seting')
        self.connect(menuTasksSetting, QtCore.SIGNAL('triggered()'), QtCore.SLOT('selctTasksSettingDialog()'))


        menubar = self.menuBar()
        menuFile = menubar.addMenu('&File')
        menuFile.addAction(menuExit)
        menuFile.addAction(menuTasksSetting)



        ## Main Widget
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        ## Main layout V
        vMainLayout = QtGui.QVBoxLayout()
        centralWidget.setLayout(vMainLayout)
        
        ## Main layout H
        hMainLayout = QtGui.QHBoxLayout()
        vMainLayout.addLayout(hMainLayout)

        # --------- Bottom text View -----------------------------
        # Bottom text view
        textView = QtGui.QTextBrowser()
        vMainLayout.addWidget(textView)

        # ----------- Left box ---------------------------------
        ## VBox left
        vListLayoutL = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutL)

        # -------------- Tree ----------------
        ### create left list
        #listview = QtGui.QTreeWidget()
        
        ### Header
        #listview.setHeaderLabel("Task")
        #vListLayoutL.addWidget(listview)


        ### Item-List
        #for item in self.tasksSettings.getStoryboard():
          #print item
          #listview.addTopLevelItem(QtGui.QTreeWidgetItem(item))
          #listview.addTopLevelItem(QtGui.QTreeWidgetItem("TEST-01"))

        # -------------- List --------------

        listview = QListWidget()
        vListLayoutL.addWidget(listview)
        ## Item-List
        for item in self.tasksSettings.getStoryboard():
          print item
          listview.insertItem(0, item)
          listview.insertItem(0, "ende")
        

        ## VBox Right
        vListLayoutR = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutR)


        # ----------- Rigth Box -------------------

        # Task name
        hLayoutName = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutName)
        nameLabel = QtGui.QLabel("Name:")
        hLayoutName.addWidget(nameLabel)
        nameLineEdit = QtGui.QLineEdit()
        hLayoutName.addWidget(nameLineEdit)



        # Task Description
        hLayoutDescription = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutDescription)
        descriptionLabel = QtGui.QLabel("Description:")
        hLayoutDescription.addWidget(descriptionLabel)
        descriptionLineEdit = QtGui.QLineEdit()
        hLayoutDescription.addWidget(descriptionLineEdit)

        ## VBox Right2
        groupBox = QtGui.QGroupBox("Todo")
        vListLayoutR2 = QtGui.QVBoxLayout()
        groupBox.setLayout(vListLayoutR2)
        vListLayoutR.addWidget(groupBox)
#        vListLayoutR.addLayout(vListLayoutR2)
#        vListLayoutR.addWidget(groupBox)  

        # Task stap typ
        hLayoutStepTyp = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutStepTyp)
        stepTypLabel = QtGui.QLabel("Step typ:")
        hLayoutStepTyp.addWidget(stepTypLabel)
        stepTypComboBox = QtGui.QComboBox()
        stepTypComboBox.addItem("replacement")
        stepTypComboBox.addItem("bash_command")
        hLayoutStepTyp.addWidget(stepTypComboBox)


        # Task Bash Command
        hLayoutBashCommand = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutBashCommand)
        bashCommandLabel = QtGui.QLabel("Bash command:")
        hLayoutBashCommand.addWidget(bashCommandLabel)
        bashCommandLineEdit = QtGui.QLineEdit()
        hLayoutBashCommand.addWidget(bashCommandLineEdit)


        # original file
        hLayoutOriginalFile = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutOriginalFile)
        originalFileLabel = QtGui.QLabel("Original file:")
        hLayoutOriginalFile.addWidget(originalFileLabel)
        originalFileLineEdit = QtGui.QLineEdit()
        hLayoutOriginalFile.addWidget(originalFileLineEdit)
        originalFilePushButton = QtGui.QPushButton("...")
        hLayoutOriginalFile.addWidget(originalFilePushButton)


        # file for replacement
        hLayoutReplacementFile = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutReplacementFile)
        replacementFileLabel = QtGui.QLabel("File for replacement:")
        hLayoutReplacementFile.addWidget(replacementFileLabel)
        replacementFileLineEdit = QtGui.QLineEdit()
        hLayoutReplacementFile.addWidget(replacementFileLineEdit)
        replacementFilePushButton = QtGui.QPushButton("...")
        hLayoutReplacementFile.addWidget(replacementFilePushButton)
        

        # Stop before execute task
        beforeCheckBox = QtGui.QCheckBox("Stop before execute task")
        vListLayoutR.addWidget(beforeCheckBox)


        ## Stop after execute task if "True"
        afterCheckBox = QtGui.QCheckBox("Stop after execute task")
        vListLayoutR.addWidget(afterCheckBox)
        
        # Statusbar
        self.statusBar().showMessage('Ready')



    ## A function with qt-slot. it's open a File-Dialog. for
    # change sie Tasks-Setting-Configuration
    @pyqtSlot()
    def selctTasksSettingDialog(self):

        print "selctTasksSettingDialog"
        filename=QtGui.QFileDialog.getOpenFileName(self, "Change tasks-Setting-Configuration", self.moldauConf.getTasksSettingsFile(),"*.*")
        print "filename: " + filename
        self.moldauConf.setTasksSettingsFile(filename)




