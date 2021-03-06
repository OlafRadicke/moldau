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
import TaskLogItem
import  array

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

    ## A list of TaskLogItem objects. For generiting minutes.
    taskLogList =  [] #director.logList

    ## Simple List
    listview = ""

    ## TaskView: This class show the taskt data.
    taskBox = ""

    ## Minutes of the proceedings as html
    minutes =  ""


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
        self.connect(savePushButton, QtCore.SIGNAL('pressed()'), QtCore.SLOT('savingMinutes()'))
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
        #print "[debug] tasksSettings.configFile" , self.tasksSettings.configFile  
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
        self.director.logList = []

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
        #selectedKasktItems = self.listview.selectedItems()
        #itemCount = selectedKasktItems.count(QtGui.QListWidgetItem)
        #print "self.listview.selectedItems().count(): ",itemCount

        for item in self.listview.selectedItems():
            print  ".." , item.text()
            todo = str(item.text())
        print "todo: ", todo
        if (todo == ""):
            QtGui.QMessageBox.warning(self, "Abort!","No task selct in list!")
            return
            
        self.director.gotoTodo(todo)
        
        #print "[debug] self.director.logList I " , self.director.logList
#        self.taskLogList = self.taskLogList + self.director.logList
        self.taskLogList = self.director.logList
        self.refreshMinutes()
        
        # set select focus
        foundItems = self.listview.findItems(self.director.lastExecuteTaktID, QtCore.Qt.MatchExactly)
        if foundItems > 0:
            index = self.listview.row(foundItems[0])
            self.listview.setCurrentRow(index, QtGui.QItemSelectionModel.ToggleCurrent)

        
    ## Open about-dialog
    @pyqtSlot()
    def about(self):
        infotext = "Arbeitstitel: Moldau \n"
        infotext = infotext + "Lizenz: GPL \n"
        infotext = infotext + "Contact: Olaf Radicke <briefkasten@olaf-radicke.de>"

        QtGui.QMessageBox.information(self, "About",infotext)

    ## Refresh minutes view.
    def refreshMinutes(self):
        html_minutes = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\
        \"http://www.w3.org/TR/html4/loose.dtd\">"
        html_minutes = html_minutes + "<html>\r <head>\r <title>Minutes</title>\r \
        </head>\r <body>\r"
        html_minutes = html_minutes + "<table border=\"1\">"
        html_minutes = html_minutes + "  <tr>"
        html_minutes = html_minutes + "    <th><b>Timestamp</b></th>"
        html_minutes = html_minutes +  "    <th><b>Task-Name</b></th>"
        html_minutes = html_minutes +  "    <th><b>Task-Typ</b></th>"
        html_minutes = html_minutes +  "    <th><b>Task-Do</b></th>"
        html_minutes = html_minutes +  "    <th><b>Task-Result</b></th>"
        html_minutes = html_minutes +  "    <th><b>Task-Note</b></th>"
        html_minutes = html_minutes +  "  </tr>"

        print "[debug] taskLogList: " , self.taskLogList
#        print "[debug] taskLogList.count(): " , self.taskLogList.count()
        for item in self.taskLogList:
            print "[debug] Item : ", item
            try:
                zeile = "  <tr>"
                zeile = zeile + "    <th>" + item.timestamp + "</th>"
                zeile = zeile + "    <th>" + item.step_id + "</th>"
                zeile = zeile + "    <th>" + item.step_type + "</th>"
                zeile = zeile + "    <th>" + item.done + "</th>"
                zeile = zeile + "    <th>" + item.result + "</th>"
                zeile = zeile + "    <th>" + item.logNote + "</th>"
                zeile = zeile + "  </tr>"
                html_minutes = html_minutes +  zeile
            except:
                print "[debug] error..."

        html_minutes = html_minutes + "</table>"
        html_minutes = html_minutes + "</body>\r </html>"

        self.textView.setHtml(html_minutes)

      

    ## Open about-dialog
    @pyqtSlot()
    def savingMinutes(self):
        print "savingMinutes()"
        filename = QtGui.QFileDialog.getSaveFileName(self, "Saving minutes", "task_minuts.html","*.html*")
        minuteFile = open(filename, 'w')
        minuteFile.write(str(self.textView.toHtml()))