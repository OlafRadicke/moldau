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

## @file zdirector.py
# @author Olaf Radicke<radicke@atix.de>

## Die Klasse führt die Regie bei der Arbeit.
class ZDirector:

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
        print("continu with todo '" + todoJump + "'....")
        ignoreTodo = True
        try:
            todoList = self.progSettings.getStoryboard()
        finally:
            return
        for todo in todoList:
            if todoJump == todo:
                ignoreTodo = False
                self.jobCenter(todo)
            elif ignoreTodo == False:
                self.jobCenter(todo)
            else:
                print("ignore todo: " + todo)

        if ignoreTodo == True:
            print("...jump target unbeknown!")
            
    ## Schaut sich an was zu tun ist und verteilt die Aufgaben an andere
    # Methoden weiter.
    def jobCenter(self, todo):

        if self.progSettings.getTodoTyp(todo) == "bash_command":
            self.bashCommand(todo)
        elif self.progSettings.getTodoTyp(todo) == "replacement":
            self.replacement(todo)
        else:
            print("Unbekanter 'stap_typ' in '" + self.progSettings.configFile  + "'.")

    ## Führt bashkomandos aus
    def bashCommand(self, todo):
        print("bashCommand:")
        command =  self.progSettings.getTodoCommand(todo)
        print(command)
        if os.system(command) == 0:
            print("...done.")
        else:
            print("...Programm ist ending with trouble, i thin. So stopping work and exit.")
            sys.exit(1)

    ## ersetzt dateien
    def replacement(self, todo):
        print("replacement:")
        try:
            oldFileName =  self.progSettings.getOldFile(todo)
            print("change file: " + oldFileName )
            oldFile = open(oldFileName,'w')

            newFileName =  self.progSettings.getNewFile(todo)
            print("with file: " + newFileName )
            newFile = open(newFileName,'r')
            fileValue = newFile.read()
            print("value: " + fileValue )
            # overwrite old fiele
            oldFile.write( fileValue )
            # closeing files
            newFile.close()
            oldFile.close()
        except:
            print "copy process is failed:", sys.exc_info()[0]
            sys.exit(1)

        print("....done.")



