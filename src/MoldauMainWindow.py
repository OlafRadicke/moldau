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

    ## Constructor
    def __init__(self, *args): 
        QtGui.QMainWindow.__init__(self, *args)

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
        taskBox = QtGui.QGroupBox("Stap list")
        vListLayoutL = QtGui.QVBoxLayout()
        taskBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(taskBox)
        

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

        # Siple List
        listview = QtGui.QListWidget()
        vListLayoutL.addWidget(listview)
        ## Item-List
        count = 0
        for item in self.tasksSettings.getStoryboard():
          print item
          listview.insertItem(count, item)
          count = count + 1
        listview.insertItem(count, "ende")
        
        # ----------- Rigth Box -------------------
        
        taskBox = TaskView()
        hMainLayout.addWidget(taskBox)

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




