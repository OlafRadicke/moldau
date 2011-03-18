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
from TaskView import TaskView



## The main window of the GUI
class MoldauMainWindow(QtGui.QMainWindow):


    ## configuraton of this applikation.
    moldauConf   = MoldauConf()
    ## The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## Simple List
    listview = ""

    ## TaskView: This class show the taskt data.
    taskBox = ""

    ## Constructor
    def __init__(self, *args): 
        QtGui.QMainWindow.__init__(self, *args)

        self.resize(800,680)
        self.setWindowTitle('Moldau')


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

        # ------------- menu end ------------

        # ----------- toolbar ---------------------
        self.toolbar = self.addToolBar('tools')
        
        toolNew = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New task', self)
        toolNew.setShortcut('Ctrl+N')
#       self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar.addAction(toolNew)

        toolRemove = QtGui.QAction(QtGui.QIcon('icons/remove.png'), 'Delete task', self)
#        toolNew.setShortcut('Ctrl+R')
#       self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar.addAction(toolRemove)

        toolDown = QtGui.QAction(QtGui.QIcon('icons/down.png'), 'Move task down', self)
#        toolNew.setShortcut('Ctrl+R')
#       self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar.addAction(toolDown)

        toolUp = QtGui.QAction(QtGui.QIcon('icons/up.png'), 'Move task up', self)
#        toolNew.setShortcut('Ctrl+R')
#       self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar.addAction(toolUp)

        toolRun = QtGui.QAction(QtGui.QIcon('icons/run.png'), 'Run task list', self)
#        toolNew.setShortcut('Ctrl+R')
#       self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar.addAction(toolRun)

        # ----------- toolbar end ------------------------



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

        # VBox left with GrouBox-frame
        resultBox = QtGui.QGroupBox("Comand result:")
        bottomLayout = QtGui.QHBoxLayout()
        resultBox.setLayout(bottomLayout)
        vMainLayout.addWidget(resultBox)

        
        # Bottom text view
        textView = QtGui.QTextBrowser()
        bottomLayout.addWidget(textView)

        # ----------- Left box ---------------------------------

        # VBox left with GrouBox-frame
        listBox = QtGui.QGroupBox("Stap list")
        vListLayoutL = QtGui.QVBoxLayout()
        listBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(listBox)
        

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

        # Label
        #stepListTypLabel = QtGui.QLabel("Step:")
        #vListLayoutL.addWidget(stepListTypLabel)

        self.listview = QtGui.QListWidget()
        vListLayoutL.addWidget(self.listview)
        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('fillTaskView()'))
#        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('selctTasksSettingDialog()'))
#        self.connect(self.listview, QtCore.SIGNAL('itemClicked()'), QtCore.SLOT('fillTaskView()'))
        ## Item-List
        count = 0
        for item in self.tasksSettings.getStoryboard():
          print item
          self.listview.insertItem(count, item)
          count = count + 1
        self.listview.insertItem(count, "ende")
        
        # ----------- Rigth Box -------------------
        
        self.taskBox = TaskView()
        hMainLayout.addWidget(self.taskBox)

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

    ## A function with qt-slot. it's fill the TaskView with data. 
    @pyqtSlot()
    def fillTaskView(self):
        for item in self.listview.selectedItems():
            print  ".." , item.text()
            self.taskBox.nameLineEdit.setText(item.text())
