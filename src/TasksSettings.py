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
from PyQt4 import QtGui, QtCore

import sys
import os.path
from TaskTyp import TaskTyp

## @file zsettings.py
# @author Olaf Radicke<radicke@atix.de>

## Class for aplication settings
class TasksSettings:

    ## constructor set name of config-file; init the ConfigParser instanc
    # and load/read the config-file
    def __init__(self, conf_file  = 'zauberformel.conf'):

        self.configFile = conf_file
        self.config = ConfigParser.ConfigParser()
#        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.configFile)

    ## generate a new config file with default and exsample values.
    def generateNewConfigFile(self):
        self.config.add_section("storyboard")
        self.config.set("storyboard", "staps", "stap_010;stap_020")

        # A example for a task with a replacement.
        self.config.add_section(u'stap_010')
        self.config.set("stap_010", "stap_typ", "replacement")
        self.config.set("stap_010", "commant", "")
        self.config.set("stap_010", "old_file", "~/var/oldfile.txt")
        self.config.set("stap_010", "new_file", "~/var/newfile.txt")
        self.config.set("stap_010", "description", "write a comment.")
        self.config.set("stap_010", "stop_before_do", "False")
        self.config.set("stap_010", "stop_after_do", "True")
        self.config.set("stap_010", "skip_stap", "False")


        # A example for a task with a bash command.
        self.config.add_section(u'stap_020')
        self.config.set("stap_020", "stap_typ", "bash_command")
        self.config.set("stap_020", "commant", "ls -lah")
        self.config.set("stap_020", "old_file", "")
        self.config.set("stap_020", "new_file", "")
        self.config.set("stap_020", "description", "write a comment.")
        self.config.set("stap_020", "stop_before_do", "False")
        self.config.set("stap_020", "stop_after_do", "True")
        self.config.set("stap_020", "skip_stap", "False")

        self.config.write(sys.stdout)
        output = open(self.configFile,'w')
        self.config.write(output)
        print "schreibe in: ", self.configFile

    ## print the config file content. For controling and debuggings.
    def print_all_confs(self):
        for section in self.config.sections():
            print section
            for option in self.config.options(section):
                print " ", option, "=", self.config.get(section, option)

    ## The function is checking the using pathes in the config of exist.
    def checkPathes(self):
        # os.path.exists("bob.txt")
        print("start self test....")
        todoList = self.getStoryboard()
        for todo in todoList:
            if self.getTodoTyp(todo) == "replacement":
                oldFileName =  self.getOldFile(todo)
                newFileName =  self.getNewFile(todo)
                if os.path.exists(oldFileName):
                    print(oldFileName + "\n     ....is OK")
                else:
                    print(oldFileName + "\n     ....NO FOUND")
                if os.path.exists(newFileName):
                    print(newFileName + "\n     ....is OK")
                else:
                    print(newFileName + "\n     ....NO FOUND")

    ## Reload the config-file.
    def reLoad(self):
        self.config.read(self.configFile)


        
# ========= get-functions ================

    ## @return get back a list of todos.
    def getStoryboard(self):
        try:
            conf_value  = self.config.get("storyboard", "staps")
            todoList  = conf_value.split(";")
            return todoList
        except Exception, e:
#        finally:
            print("Das storybord in der Konfiguration schein falsch gesetzt zu sein.")
            print("Prüfe sie die Datei: " + self.configFile)
            raise "get storyboard failure"
            print(e)
#            sys.exit(0)

    ##  @param todo a todo in the list of "Storyboard".
    # @return get a class of TaskTyp
    def getTaskTyp(self, todo):
        taskTyp = TaskTyp()
        taskTyp.ID = todo
        taskTyp.Depiction = self.getDescription(todo)
        taskTyp.TodoTyp = self.getTodoTyp(todo)
        taskTyp.BashCommand = self.getTodoCommand(todo)
        taskTyp.OldFile = self.getOldFile(todo)
        taskTyp.NewFile  = self.getNewFile(todo)
        taskTyp.StopBefore = self.isStopBeforeDo(todo)
        taskTyp.StopAfter = self.isStopAfterDo(todo)
        taskTyp.SkipStap = self.isSkipStap(todo)
        return taskTyp
      
    ##
    # @param todo a todo in the list of "Storyboard".
    # @return get the typ of a todo.
    def getTodoTyp(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "stap_typ")
        except:
            print "[OR20110320_2021_01]"
            conf_value  = "bash_command"
        return conf_value

    ##
    # @param todo a todo in the list of "Storyboard".
    # @return get the command of a bash comand todo.
    def getTodoCommand(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "commant")
        except:
            print "[OR20110320_2021_02]"
            conf_value  = ""
        return conf_value

    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return the file name which we would like remove.
    def getOldFile(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "old_file")
        except:
            print "[OR20110320_2021_03]"
            conf_value  = ""
        return conf_value

    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return the file name which we over write the old file.
    def getNewFile(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "new_file")
        except:
            print "[OR20110320_2021_04]"
            conf_value  = ""
        return conf_value

    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return the description of a stap.
    def getDescription(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "description")
        except:
            print "[OR20110320_2021_05]"
            conf_value  = ""
        return conf_value


    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return "True" if stop by stap before do the task.
    # Else return "False".
    def isStopBeforeDo(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "stop_before_do")
        except:
            print "[OR20110320_2021_06]"
            conf_value  = "False"
        return conf_value

    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return "True" if stop by stap after do the task.
    # Else return "False".
    def isStopAfterDo(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "stop_after_do")
        except:
            print "[OR20110320_2021_07]"
            conf_value  =  "False"
        return conf_value
        
    ##
    # @param todo a todo in the list of "Storyboard".
    # @return return "True" if skip this stap.
    # Else return "False".
    def isSkipStap(self, todo):
        try:
            conf_value  = self.config.get(str(todo), "skip_stap")
        except:
            print "[OR20110320_2021_06]"
            conf_value  =  "False"
        return conf_value


# ========= set-functions ================

    def setConfFile(self, value):
        self.configFile = value
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)
        print "Read: " , self.configFile
        print "Storyboard: " , self.getStoryboard()



    ##  Sat and safing a task-class.
    # @param taskTyp Ths task-class is safing.
    def setTaskTyp(self, taskTyp):
        self.config.set(taskTyp.ID, "description", taskTyp.Depiction)
        self.config.set(str(taskTyp.ID), "stap_typ", str(taskTyp.TodoTyp))
        self.config.set(str(taskTyp.ID), "commant", str(taskTyp.BashCommand))
        self.config.set(str(taskTyp.ID), "old_file", str(taskTyp.OldFile))
        self.config.set(str(taskTyp.ID), "new_file", str(taskTyp.NewFile))
        self.config.set(str(taskTyp.ID), "stop_before_do", str(taskTyp.StopBefore))
        self.config.set(str(taskTyp.ID), "stop_after_do", str(taskTyp.StopAfter))
        self.config.set(str(taskTyp.ID), "skip_stap", str(taskTyp.SkipStap))

        self.config.write(sys.stdout)
        output = open(self.configFile,'w')
        self.config.write(output)
        print "schreibe in: ", self.configFile        