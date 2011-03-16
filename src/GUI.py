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
class MainWindow(QtGui.QMainWindow):

    ## pseudo data
    list_data  = [1,2,3,4]
    ## configuraton of this applikation.
    moldauConf   = MoldauConf()
    ## The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## Constructor
    def __init__(self, *args): 
        QtGui.QWidget.__init__(self, *args) 


        # pseudo data
        lm = MyListModel(self.list_data, self)

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

        ## create table
        listview = QtGui.QListView()
        listview.setModel(lm)
        vListLayoutL.addWidget(listview)


        ## VBox Right
        vListLayoutR = QtGui.QVBoxLayout()
        hMainLayout.addLayout(vListLayoutR)

        ## create Rigth table
        listviewR = QtGui.QListView()
        listviewR.setModel(lm)
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


## Helper class 
class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain
 
    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else: 
            return QtCore.QVariant()


def startGUI():
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

