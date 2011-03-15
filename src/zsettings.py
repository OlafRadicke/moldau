#! /usr/bin/env python
# -*- coding: utf-8 -*-

 ###########################################################################
 #   Copyright (C) 2010 by                                                 #
 #   Atix <info@atix.de>                                                   #
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
 ###########################################################################

import ConfigParser
import sys
import os.path

## @file zsettings.py
# @author Olaf Radicke<radicke@atix.de>

## Class for aplication settings
class ZSettings:

    ## constructor set name of config-file; init the ConfigParser instanc
    # and load/read the config-file
    def __init__(self, conf_file  = 'zauberformel.conf'):

        self.configFile = conf_file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)

    ## generate a new config file with default and exsample values.
    def generateNewConfigFile(self):
        self.config.add_section("storyboard")
        self.config.set("storyboard", "staps", "stap_010;stap_020")


        self.config.add_section("stap_010")
        self.config.set("stap_010", "stap_typ", "replacement")
        self.config.set("stap_010", "old_file", "~/var/oldfile.txt")
        self.config.set("stap_010", "new_file", "~/var/newfile.txt")
        self.config.set("stap_010", "description", "write a comment.")


        self.config.add_section("stap_020")
        self.config.set("stap_020", "stap_typ", "bash_command")
        self.config.set("stap_020", "commant", "ls -lah")
        self.config.set("stap_020", "description", "write a comment.")

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

    def setConfFile(self, value):
        self.configFile = value
        
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

    ##
    # @param todo  the todo from the config-file which is meaning.
    # @return get the typ of a todo.
    def getTodoTyp(self, todo):
        conf_value  = self.config.get(todo, "stap_typ")
        return conf_value

    ##
    # @param todo  the todo from the config-file which is meaning.
    # @return get the command of a bash comand todo.
    def getTodoCommand(self, todo):
        conf_value  = self.config.get(todo, "commant")
        return conf_value

    ##
    # @param todo  the todo from the config-file which is meaning.
    # @return return the file name which we would like remove.
    def getOldFile(self, todo):
        conf_value  = self.config.get(todo, "old_file")
        return conf_value

    ##
    # @param todo  the todo from the config-file which is meaning.
    # @return return the file name which we would like remove.
    def getNewFile(self, todo):
        conf_value  = self.config.get(todo, "new_file")
        return conf_value

    ##
    # @param todo  the todo from the config-file which is meaning.
    # @return return the description of a stap.
    def getDescription(self, todo):
        conf_value  = self.config.get(todo, "description")
        return conf_value



