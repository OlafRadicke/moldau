#!/usr/bin/python
# -*- coding: utf-8 -*-


 ###########################################################################
 #   Copyright (C) 2010 by ATIX AG, Olaf Radicke                           #
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
 ###########################################################################

import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from MoldauConf import MoldauConf
from TasksSettings import TasksSettings
from TaskView import TaskView
from TaskTyp import TaskTyp
from Director import Director

## @file TaskTyp.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>

## The main window of the GUI
class MoldauMainWindow(QtGui.QMainWindow):


    ## configuraton of this applikation.
    moldauConf   = MoldauConf()
    ## The setings  of taskts.
    tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())

    ## Class controling the task runnings.
    director = Director(tasksSettings)

    ## Simple List
    listview = ""

    ## TaskView: This class show the taskt data.
    taskBox = ""

    ## Minutes of the proceedings
    minutes = ""

    ## This QTextBrowser show the minutes of the proceedings
    textView = ""

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
        menuFile.addAction(menuTasksSetting)
        menuFile.addAction(menuExit)


        ## Menue-item for change the task stetting file.
        menuInfoAbout = QtGui.QAction( 'About', self)
        menuInfoAbout.setShortcut('Ctrl+I')
        menuInfoAbout.setStatusTip('About this programm.')
        self.connect(menuInfoAbout, QtCore.SIGNAL('triggered()'), QtCore.SLOT('about()'))


        menuFile = menubar.addMenu('&Info')
        menuFile.addAction(menuInfoAbout)

        # ------------- menu end ------------

        # ----------- toolbar ---------------------
        self.toolbar = self.addToolBar('tools')
        
        toolNew = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New task', self)
        toolNew.setShortcut('Ctrl+N')
        self.connect(toolNew, QtCore.SIGNAL('triggered()'), QtCore.SLOT('newTasksDialog()'))
        self.toolbar.addAction(toolNew)

        toolRemove = QtGui.QAction(QtGui.QIcon('icons/remove.png'), 'Delete task', self)
        toolNew.setShortcut('Ctrl+X')
        self.connect(toolRemove, QtCore.SIGNAL('triggered()'), QtCore.SLOT('deleteTask()'))
        self.toolbar.addAction(toolRemove)

        toolDown = QtGui.QAction(QtGui.QIcon('icons/down.png'), 'Move task down', self)
        toolNew.setShortcut('Ctrl+D')
        self.connect(toolDown, QtCore.SIGNAL('triggered()'), QtCore.SLOT('laterInList()'))
        self.toolbar.addAction(toolDown)

        toolUp = QtGui.QAction(QtGui.QIcon('icons/up.png'), 'Move task up', self)
        toolNew.setShortcut('Ctrl+U')
        self.connect(toolUp, QtCore.SIGNAL('triggered()'), QtCore.SLOT('earlierInList()'))
        self.toolbar.addAction(toolUp)

        toolRun = QtGui.QAction(QtGui.QIcon('icons/run.png'), 'Run task list', self)
        toolNew.setShortcut('Ctrl+G')
        self.connect(toolRun, QtCore.SIGNAL('triggered()'), QtCore.SLOT('directorRun()'))
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
        bottomLayout = QtGui.QVBoxLayout()
        resultBox.setLayout(bottomLayout)
        vMainLayout.addWidget(resultBox)

        
        # Bottom text view
        self.textView = QtGui.QTextBrowser()
        bottomLayout.addWidget(self.textView)


        # Button bar
        hLayoutButtonBar = QtGui.QHBoxLayout()
        bottomLayout.addLayout(hLayoutButtonBar)
        clearPushButton = QtGui.QPushButton("Clear minutes")
        self.connect(clearPushButton, QtCore.SIGNAL('pressed()'), QtCore.SLOT('clearMinutes()'))
        hLayoutButtonBar.addWidget(clearPushButton)
        savePushButton = QtGui.QPushButton("Save minutes as...")
        hLayoutButtonBar.addWidget(savePushButton)


        # ----------- Left box ---------------------------------

        # VBox left with GrouBox-frame
        listBox = QtGui.QGroupBox("Stap list")
        listBox.setMaximumWidth(250)
        vListLayoutL = QtGui.QVBoxLayout()
        listBox.setLayout(vListLayoutL)
        hMainLayout.addWidget(listBox)
        

        # -------------- List --------------

        # Label
        #stepListTypLabel = QtGui.QLabel("Step:")
        #vListLayoutL.addWidget(stepListTypLabel)

        self.listview = QtGui.QListWidget()
        vListLayoutL.addWidget(self.listview)
        self.connect(self.listview, QtCore.SIGNAL('itemSelectionChanged()'), QtCore.SLOT('fillTaskView()'))

        #count = 0
        #for item in self.tasksSettings.getStoryboard():
          #print item
          #self.listview.insertItem(count, item)
          #count = count + 1
        
        # ----------- Rigth Box -------------------
        
        self.taskBox = TaskView()
        hMainLayout.addWidget(self.taskBox)
        self.taskBox.setMoldauConf(self.moldauConf)
        self.taskBox.setTasksSettings(self.tasksSettings)
        self.connect(self.taskBox , QtCore.SIGNAL('taskIsChange()'), QtCore.SLOT('refreshTaskList()'))

        # Statusbar
        self.statusBar().showMessage('Ready')
        # Item-List
        self.refreshTaskList()

        ## @todo Only for demo!
        self.__minutesExsample()

    ## A function with qt-slot. it's creade a new task.
    @pyqtSlot()
    def newTasksDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, "New Task", "Task name:", 0)
        if ok != True :
          print "[debug] if: " , text, ok
          return
        else:
          print "[debug] else: " , text, ok
          taskTyp = TaskTyp()
          taskTyp.ID = text
          self.tasksSettings.addTaskTyp(taskTyp)
          self.refreshTaskList()
          self.taskBox.setTasksSettings(self.tasksSettings)
      
    ## A function with qt-slot. it's open a File-Dialog. for
    # change sie Tasks-Setting-Configuration
    @pyqtSlot()
    def selctTasksSettingDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Change tasks-Setting-Configuration", self.moldauConf.getTasksSettingsFile(),"*.*")
        self.statusBar().showMessage(str("try open task setting file: " + filename))
        self.moldauConf.setTasksSettingsFile(str(filename))
        self.tasksSettings.setConfFile(str(filename))
        print "[debug] tasksSettings.configFile" , self.tasksSettings.configFile  
        self.listview.clear ()
        # refill item-List
        count = 0
        for item in self.tasksSettings.getStoryboard():
            print item
            self.listview.insertItem(count, item)
            count = count + 1
        
    ## Refrash the list of tasks.
    @pyqtSlot()
    def refreshTaskList(self):
        self.tasksSettings.reLoad()
        self.taskBox.setTasksSettings(self.tasksSettings)
        self.listview.clear ()
        count = 0
        for item in self.tasksSettings.getStoryboard():
            print "[debug] ", item
            self.listview.insertItem(count, item)
            count = count + 1


    ## A function with qt-slot. it's fill the TaskView with data. 
    @pyqtSlot()
    def fillTaskView(self):
        todo = ""
        for item in self.listview.selectedItems():
            print  "[debug] .." , item.text()
            todo = item.text()

        if( todo == "" ):
            self.statusBar().showMessage('No ToDo select...')
        else:
          taskTyp = self.tasksSettings.getTaskTyp(todo)
          self.taskBox.setTaskTyp(taskTyp)

    ## Function clear the minutes in the textView
    @pyqtSlot()
    def clearMinutes(self):
        print "[debug] clearMinutes..."
        self.minutes = ""
        self.textView.setHtml(self.minutes)

    ## Function delete a task
    @pyqtSlot()
    def deleteTask(self):
        print "[debug] deleteTask"
        todo = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text()
            todo = item.text()

        if( todo == "" ):
            self.statusBar().showMessage('No ToDo select...')
        else:
          taskTyp = self.tasksSettings.getTaskTyp(todo)
          self.tasksSettings.deleteTask(taskTyp)
          self.refreshTaskList()


    ## Function / slot set a task on a later place in list.
    @pyqtSlot()
    def earlierInList(self):
        print "[debug] earlierInList"
        todo = ""
#        listWidgetItem = QtGui.QListWidgetItem()
        for item in self.listview.selectedItems():
            print  "[debug] .." , item.text()
            todo = item.text()
#            listWidgetItem = item

        if( todo == "" ):
            self.statusBar().showMessage('No ToDo select...')
        else:
          taskTyp = self.tasksSettings.getTaskTyp(todo)
          self.tasksSettings.earlierInList(taskTyp)
          self.refreshTaskList()

          # set select focus
          foundItems = self.listview.findItems(todo, QtCore.Qt.MatchExactly)
          if foundItems > 0:
              index = self.listview.row(foundItems[0])
              self.listview.setCurrentRow(index, QtGui.QItemSelectionModel.ToggleCurrent)
                  
    ## Function / slot set a task on a later place in list.
    @pyqtSlot()
    def laterInList(self):
        print "[debug] laterInList"
        todo = ""
#        listWidgetItem = QtGui.QListWidgetItem()
        for item in self.listview.selectedItems():
            print  ".." , item.text()
            todo = item.text()
#            listWidgetItem = item

        if( todo == "" ):
            self.statusBar().showMessage('No ToDo select...')
        else:
          taskTyp = self.tasksSettings.getTaskTyp(todo)
          self.tasksSettings.laterInList(taskTyp)
          self.refreshTaskList()

          # set select focus
          foundItems = self.listview.findItems(todo, QtCore.Qt.MatchExactly)
          if foundItems > 0:
              index = self.listview.row(foundItems[0])
              self.listview.setCurrentRow(index, QtGui.QItemSelectionModel.ToggleCurrent)
        
    ## Function / slot is start the task executing,
    @pyqtSlot()
    def directorRun(self):
        print "[debug] directorRun"
        todo = ""
        for item in self.listview.selectedItems():
            print  ".." , item.text()
            todo = item.text()
        self.director.gotoTodo(todo)
        
    ## Open about-dialog
    @pyqtSlot()
    def about(self):
        pass
        #msgBox = QtGui.QMssageBox(self)
        #msgBox.setText("About");
        #msgBox.setInformativeText("Contact: Olaf Radicke <briefkasten@olaf-radicke.de>");
        #msgBox.setStandardButtons(QMessageBox.Ok);
        
        #msgBox.setDefaultButton(QMessageBox::Save);
        #int ret = msgBox.exec();

        infotext = "Arbeitstitel: Moldau \n"
        infotext = infotext + "Lizenz: GPL \n"
        infotext = infotext + "Contact: Olaf Radicke <briefkasten@olaf-radicke.de>"

        QtGui.QMessageBox.information(self, "About",infotext)

      
    ## Only a fake-output, as exsample. 
    def __minutesExsample(self):

        textExample =  "<table border=\"1\">"
        textExample = textExample +  "  <tr>"
        textExample = textExample +  "    <th><b>Timestamp</b></th>"
        textExample = textExample +  "    <th><b>Task-Name</b></th>"
        textExample = textExample +  "    <th><b>Task-Typ</b></th>"
        textExample = textExample +  "    <th><b>Task-Do</b></th>"
        textExample = textExample +  "    <th><b>Task-Result</b></th>"
        textExample = textExample +  "  </tr>"
        textExample = textExample +  "  <tr>"
        textExample = textExample +  "    <td>2011-03-20-21:43</td>"
        textExample = textExample +  "    <td>Task_01</td>"
        textExample = textExample +  "    <td>bash_command</td>"
        textExample = textExample +  "    <td>mkdir ./test-dir</td>"
        textExample = textExample +  "    <td>okay</td>"
        textExample = textExample +  "  </tr>"
        textExample = textExample +  "  <tr>"
        textExample = textExample +  "    <td>2011-03-20-21:44</td>"
        textExample = textExample +  "    <td>Task_02</td>"
        textExample = textExample +  "    <td>bash_command</td>"
        textExample = textExample +  "    <td>rm ./testdata-2.txt</td>"
        textExample = textExample +  "    <td>rm: cannot remove `./testdata-2.txt': No such file or directory</td>"
        textExample = textExample +  "  </tr>"
        textExample = textExample +  "  <tr>"
        textExample = textExample +  "    <td>2011-03-20-21:46</td>"
        textExample = textExample +  "    <td>Task_03</td>"
        textExample = textExample +  "    <td>bash_command</td>"
        textExample = textExample +  "    <td>cd ./testdata-2.txt</td>"
        textExample = textExample +  "    <td>bash: cd: ./testdata-2.txt: No such file or directory</td>"
        textExample = textExample +  "  </tr>"
        self.minutes = textExample +  "</table>"

        self.textView.setHtml(self.minutes)      
