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
from TaskTyp import TaskTyp



## This Widget view the data of a task
class TaskView(QtGui.QGroupBox):


    ## Frame style
    owneFramStyleSheet = "QGroupBox{border:2px solid gray;border-radius:7px;margin-top: 1ex;} \
    QGroupBox::title{subcontrol-origin: margin;subcontrol-position:top center;padding:0 3px;} "

    ## Typ:.MoldauConf.  configuraton of this applikation.
    moldauConf   = MoldauConf()
    
    ## Typ:.TasksSettings.  The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## TaskTyp
    task = TaskTyp()

    ## Typ:.LineEdit.  QtGui.QLineEdit: Text fild for name of Task
    nameLineEdit = ""

    ## Typ:.LineEdit.  LineEdit for description.
    descriptionLineEdit = ""

    ## Typ:.ComboBox.  ComboBox show the typ of Todo
    todoTypComboBox = ""

    ## Typ:.LineEdit.  The bash command 
    bashCommandLineEdit = ""

    ## Typ:.LineEdit.  original file path.
    originalFileLineEdit = ""

    ## Typ:.LineEdit.   The path too file for substitude sie original old file.
    replacementFileLineEdit = ""

    ## Typ: CheckBox.  Is stoped before execute task, if "True"
    beforeCheckBox = ""

    ##  Typ: CheckBox. Stop after execute task if "True"
    afterCheckBox = ""

    ## Skip this task if set "True"
    skipCheckBox = ""


    taskIsChange = QtCore.pyqtSignal()

    ## Constructor
    def __init__(self):
        QtGui.QGroupBox.__init__(self)


        # ----------- Rigth Box -------------------
        # VBox Right with GrouBox-frame
        self.setTitle("Stap details")
        self.setStyleSheet(self.owneFramStyleSheet)
        vListLayoutR = QtGui.QVBoxLayout()
        self.setLayout(vListLayoutR)

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
        self.descriptionLineEdit = QtGui.QLineEdit()
        hLayoutDescription.addWidget(self.descriptionLineEdit)

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
        self.todoTypComboBox = QtGui.QComboBox()
        self.todoTypComboBox.addItem("replacement")
        self.todoTypComboBox.addItem("bash_command")
        self.connect(self.todoTypComboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), QtCore.SLOT('todoTypComboBoxChange(QString)'))
        hLayoutStepTyp.addWidget(self.todoTypComboBox)


        # Task Bash Command
        hLayoutBashCommand = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutBashCommand)
        bashCommandLabel = QtGui.QLabel("Bash command:")
        hLayoutBashCommand.addWidget(bashCommandLabel)
        self.bashCommandLineEdit = QtGui.QLineEdit()
        hLayoutBashCommand.addWidget(self.bashCommandLineEdit)


        # original file
        hLayoutOriginalFile = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutOriginalFile)
        originalFileLabel = QtGui.QLabel("Original file:")
        hLayoutOriginalFile.addWidget(originalFileLabel)
        self.originalFileLineEdit = QtGui.QLineEdit()
        hLayoutOriginalFile.addWidget(self.originalFileLineEdit)
        originalFilePushButton = QtGui.QPushButton("...")
        hLayoutOriginalFile.addWidget(originalFilePushButton)


        # file for replacement
        hLayoutReplacementFile = QtGui.QHBoxLayout()
        vListLayoutR2.addLayout(hLayoutReplacementFile)
        replacementFileLabel = QtGui.QLabel("File for replacement:")
        hLayoutReplacementFile.addWidget(replacementFileLabel)
        self.replacementFileLineEdit = QtGui.QLineEdit()
        hLayoutReplacementFile.addWidget(self.replacementFileLineEdit)
        replacementFilePushButton = QtGui.QPushButton("...")
        hLayoutReplacementFile.addWidget(replacementFilePushButton)
        


        ## VBox Right3
        doControlGroupBox = QtGui.QGroupBox("Task control")
        vListLayoutR3 = QtGui.QVBoxLayout()
        doControlGroupBox.setLayout(vListLayoutR3)
        vListLayoutR.addWidget(doControlGroupBox)

        # Stop before execute task
        self.beforeCheckBox = QtGui.QCheckBox("Stop before execute task")
        vListLayoutR3.addWidget(self.beforeCheckBox)

        ## Stop after execute task if "True"
        self.afterCheckBox = QtGui.QCheckBox("Stop after execute task")
        vListLayoutR3.addWidget(self.afterCheckBox)

        ## Skip this task if set "True"
        self.skipCheckBox = QtGui.QCheckBox("Skip this task")
        vListLayoutR3.addWidget(self.skipCheckBox)



        # Button bar
        hLayoutButtonBar = QtGui.QHBoxLayout()
        vListLayoutR.addLayout(hLayoutButtonBar)
        resetPushButton = QtGui.QPushButton("Reset")
        self.connect(resetPushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('resetTaskChanges()'))
        hLayoutButtonBar.addWidget(resetPushButton)
        
        safePushButton = QtGui.QPushButton("Safe")
        self.connect(safePushButton, QtCore.SIGNAL('clicked()'), QtCore.SLOT('safeTaskChanges()'))
        hLayoutButtonBar.addWidget(safePushButton)

    ## @return Get TasksSetting-Object
    def getTasksSettings():
        return self.tasksSettings

    ## Set configuraton of this applikation.
    def setMoldauConf(self, conf):
        self.moldauConf = conf

    ## Set the setings  of taskts.
    def setTasksSettings(self, setings):
        tasksSettings = setings

    ## Set the task and show his data.
    def setTaskTyp(self, task):
        self.task = task
        self.nameLineEdit.setText(task.ID)
        self.descriptionLineEdit.setText(task.Depiction)

        item_index = self.todoTypComboBox.findText(task.TodoTyp)
        if (item_index == -1):
            self.todoTypComboBox.addItem(task.TodoTyp)
        else:
            self.todoTypComboBox.setCurrentIndex(item_index)

        self.bashCommandLineEdit.setText(task.BashCommand)
        self.originalFileLineEdit.setText(task.OldFile)
        self.replacementFileLineEdit.setText(task.NewFile)

        if (task.StopBefore == "False"):
            self.beforeCheckBox.setChecked(False)
        else:
            self.beforeCheckBox.setChecked(True)

        if (task.StopAfter == "False"):
            self.afterCheckBox.setChecked(False)
        else:
            self.afterCheckBox.setChecked(True)

        if (task.SkipStap == "False"):
            self.skipCheckBox.setChecked(False)
        else:
            self.skipCheckBox.setChecked(True)

        index_text = self.todoTypComboBox.currentText()
        self.todoTypComboBoxChange(index_text)

    ## it is action if todoTypComboBox change
    @pyqtSlot(QtCore.QString)
    def todoTypComboBoxChange(self, text):
        if (text == "bash_command"):
            self.originalFileLineEdit.setEnabled(False)
            self.replacementFileLineEdit.setEnabled(False)
            self.bashCommandLineEdit.setEnabled(True)
        elif(text == "replacement"):
            self.originalFileLineEdit.setEnabled(True)
            self.replacementFileLineEdit.setEnabled(True)
            self.bashCommandLineEdit.setEnabled(False)
        else:
            print "[OR2011_0320_2045]"


    ## Safe the task changes.
    @pyqtSlot()
    def safeTaskChanges(self):
        print "safeTaskChanges"

        taskTyp = TaskTyp()
        taskTyp.ID = str(self.nameLineEdit.text())
        taskTyp.Depiction = str(self.descriptionLineEdit.text())
        taskTyp.TodoTyp = str(self.todoTypComboBox.currentText())
        taskTyp.BashCommand = str(self.bashCommandLineEdit.text())
        taskTyp.OldFile = str(self.originalFileLineEdit.text())
        taskTyp.NewFile = str(self.replacementFileLineEdit.text())
        taskTyp.StopBefore = str(self.beforeCheckBox.isChecked())
        taskTyp.StopAfter = str(self.afterCheckBox.isChecked())
        taskTyp.SkipStap = str(self.skipCheckBox.isChecked())

        self.tasksSettings.setTaskTyp(taskTyp)
        self.taskIsChange.emit()



    ## Safe the task changes.
    @pyqtSlot()
    def resetTaskChanges(self):
        self.setTaskTyp(self.task)
           
          