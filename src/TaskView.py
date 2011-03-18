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




## This Widget view the data of a task
class TaskView(QtGui.QGroupBox):


    ## configuraton of this applikation.
    moldauConf   = MoldauConf()
    ## The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## QtGui.QLineEdit: Text fild for name of Task
    nameLineEdit = ""

    ## Constructor
    def __init__(self):
        QtGui.QGroupBox.__init__(self)


        # ----------- Rigth Box -------------------
        # VBox Right with GrouBox-frame
#        taskBox = QtGui.QGroupBox("Stap details")
        self.setTitle("Stap details")
        vListLayoutR = QtGui.QVBoxLayout()
        self.setLayout(vListLayoutR)
#        hMainLayout.addWidget(taskBox)

        # Task name
        hLayoutName = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutName)
        nameLabel = QtGui.QLabel("Name:")
        hLayoutName.addWidget(nameLabel)
        self.nameLineEdit = QtGui.QLineEdit()
        self.nameLineEdit.setReadOnly(True)
        hLayoutName.addWidget(self.nameLineEdit)



        # Task Description
        hLayoutDescription = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutDescription)
        descriptionLabel = QtGui.QLabel("Description:")
        hLayoutDescription.addWidget(descriptionLabel)
        descriptionLineEdit = QtGui.QLineEdit()
        hLayoutDescription.addWidget(descriptionLineEdit)

        ## VBox Right2
        toDoGroupBox = QtGui.QGroupBox("Todo")
        vListLayoutR2 = QtGui.QVBoxLayout()
        toDoGroupBox.setLayout(vListLayoutR2)
        vListLayoutR.addWidget(toDoGroupBox)


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
        


        ## VBox Right3
        doControlGroupBox = QtGui.QGroupBox("Task control")
        vListLayoutR3 = QtGui.QVBoxLayout()
        doControlGroupBox.setLayout(vListLayoutR3)
        vListLayoutR.addWidget(doControlGroupBox)

        # Stop before execute task
        beforeCheckBox = QtGui.QCheckBox("Stop before execute task")
        vListLayoutR3.addWidget(beforeCheckBox)

        ## Stop after execute task if "True"
        afterCheckBox = QtGui.QCheckBox("Stop after execute task")
        vListLayoutR3.addWidget(afterCheckBox)

        ## Skip this task if set "True"
        skipCheckBox = QtGui.QCheckBox("Skip this task")
        vListLayoutR3.addWidget(skipCheckBox)



        # Button bar
        hLayoutButtonBar = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutButtonBar)
        resetPushButton = QtGui.QPushButton("Reset")
        hLayoutButtonBar.addWidget(resetPushButton)
        savePushButton = QtGui.QPushButton("Save")
        hLayoutButtonBar.addWidget(savePushButton)

