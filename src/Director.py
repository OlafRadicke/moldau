#! /usr/bin/env python
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

import ConfigParser
import sys
import os
import TaskLogItem
from datetime import datetime, date, time

## @file Director.py
# @author Olaf Radicke<radicke@atix.de>

## Die Klasse führt die Regie bei der Arbeit.
class Director:

    logList = []

    lastExecuteTaktID = ""

    ## constructor set a instac of a ZSettings class
    def __init__(self, settings):
        self.progSettings = settings

    ## Begint die Aufgabenliste ab zu arbeiten
    def start(self):
        print("start todo....")
        try:
            todoList = self.progSettings.getStoryboard()
        finally:
            return
        
        for todo in todoList:
            self.jobCenter(todo)

    ## jump to decided point
    def gotoTodo(self, todoJump):
        #print("continu with todo '" + todoJump + "'....")
        ignoreTodo = True
        result = True

        todoList = self.progSettings.getStoryboard()
        #print "[debug] todoList: " , todoList


        for todo in todoList:
          
            # is this the jump in point...
            if todoJump == todo:
                #print "[debug] ...if todoJump == todo"
                ignoreTodo = False
                # get the todo object
                taskTyp = self.progSettings.getTaskTyp(todo)
                result = self.jobCenter(taskTyp)
                if(taskTyp.StopAfter == "True"):
                    self.lastExecuteTaktID = taskTyp.ID
                    return
            # is this todo after jump in point, go...
            elif ignoreTodo == False:
                #print "[debug] ...elif ignoreTodo == False"
                # get the todo object
                taskTyp = self.progSettings.getTaskTyp(todo)
                self.lastExecuteTaktID = taskTyp.ID
                if(taskTyp.StopBefore == "True"):
                    return
                result = self.jobCenter(taskTyp)
                if(taskTyp.StopAfter == "True"):
                    return
            # it's not jump in poinz oder later. So ignore...
            else:
                print("ignore todo: " + todo)
            if (result == False):
                return

        if ignoreTodo == True:
            print("...jump target unbeknown!")
            
    ## Schaut sich an was zu tun ist und verteilt die Aufgaben an andere
    # Methoden weiter.
    # @return True if successful.
    def jobCenter(self, taskTyp):
        # Item for Logging
        taskLogItem = TaskLogItem.TaskLogItem()
        
        taskLogItem.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        #print "[debug] direktor -> todo: " , taskTyp.ID
        taskLogItem.step_id = taskTyp.ID
        taskLogItem.step_type = taskTyp.TodoTyp

        if taskLogItem.step_type == "bash_command":
            result = self.bashCommand(taskTyp, taskLogItem)
        elif taskLogItem.step_type == "replacement":
            result = self.replacement(taskTyp, taskLogItem)
        else:
            print("Unbekanter 'stap_typ' in '" + self.progSettings.configFile  + "'.")
            taskLogItem.logNote = "Unbekanter 'stap_typ' in '" + self.progSettings.configFile  + "'."
            taskLogItem.done = "pass"
            self.logList.append(taskLogItem)
        return result

    ## Führt bashkomandos aus
    # @return True if successful.
    def bashCommand(self, taskTyp, taskLogItem):
        taskLogItem.done = taskTyp.BashCommand
        #print "bashCommand:", taskTyp.BashCommand
        if os.system(taskTyp.BashCommand) == 0:
            print("...done.")
            taskLogItem.result = "...done."
            self.logList.append(taskLogItem)
            return True
        else:
            print("...Programm ist ending with trouble, i thin. So stopping work and exit.")
            taskLogItem.result = "...Programm ist ending with trouble, i thin. So stopping work and exit."
            self.logList.append(taskLogItem)
            return False

    ## ersetzt dateien
    # @param taskTyp a TaskTyp Object represent info about a task.
    # @param taskLogItem TaskLogItem Object info represent info about result of task run.
    # @return True if successful.
    def replacement(self, taskTyp, taskLogItem):
        #print("replacement:")
        #print "[debug] replacement I: ", taskLogItem
        try:
            oldFileName =  taskTyp.OldFile
            print("change file: " + oldFileName )
            newFileName =  taskTyp.NewFile
            print("with file: " + newFileName )
            taskLogItem.done = "replacement: " + oldFileName + " < " + newFileName
            oldFile = open(oldFileName,'w')
            newFile = open(newFileName,'r')
            fileValue = newFile.read()
            print("[debug] value: " + fileValue )
            # overwrite old fiele
            oldFile.write( fileValue )
            # closeing files
            newFile.close()
            oldFile.close()
        except:
            print "copy process is failed:", sys.exc_info()[0]
            taskLogItem.result = "copy process is failed:", sys.exc_info()[0]
            self.logList.append(taskLogItem)
            #print "[debug] replacement II: ", taskLogItem
            return False

        print("....done.")
        taskLogItem.result = "....done."
        self.logList.append(taskLogItem)
        return True



