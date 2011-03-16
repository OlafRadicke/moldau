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

        ## Main layout
        hMainLayout = QtGui.QHBoxLayout()
        centralWidget.setLayout(hMainLayout)

        ## VBox left
        vListLayoutL = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutL)

        ## create left list
        listview = QtGui.QListView()
        itemModelL = QtGui.QStandardItemModel()
        itemModelL.appendRow(QtGui.QStandardItem("TEST-1"))
        itemModelL.appendRow(QtGui.QStandardItem("TEST-2"))
        listview.setModel(itemModelL)
        vListLayoutL.addWidget(listview)


        ## VBox Right
        vListLayoutR = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutR)

        ## create Rigth table
        listviewR = QtGui.QListView()
        itemModel = QtGui.QStandardItemModel()
        itemModel.appendRow(QtGui.QStandardItem("TEST"))
        listviewR.setModel(itemModel)
        vListLayoutR.addWidget(listviewR)

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




