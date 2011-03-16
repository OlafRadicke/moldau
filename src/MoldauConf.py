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
import os.path

## @file MoldauConf.py
# @author Olaf Radicke<radicke@atix.de>

## Class for general aplication settings.
class MoldauConf:

    ## constructor set name of config-file; init the ConfigParser instanc
    # and load/read the config-file
    def __init__(self, conf_file  = '~/.moldau.conf'):

        self.configFile = os.path.abspath(os.path.expanduser(conf_file))
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)

    ## generate a new config file with default and exsample values.
    def generateNewConfigFile(self):

        # set section "main"
        self.config.add_section("main")
        
        self.config.set("main", "logfile", os.path.abspath(os.path.expanduser("~/moldau.log")))
        self.config.set("main", "tasks_settings_file", os.path.abspath(os.path.expanduser("~/taskssettings.moldau")))

        # set section "QTGUI"
        self.config.add_section("QTGUI")
        
        self.config.set("QTGUI", "mainwindo_size", "null")

        self.config.write(sys.stdout)
        output = open(self.configFile,'w')
        self.config.write(output)

    ## print the config file content. For controling and debuggings.
    # @retun return_string
    def print_all_confs(self):
      
        return_string = ""
        for section in self.config.sections():
            print section
            return_string = return_string + section + "/n"
            for option in self.config.options(section):
                print " ", option, "=", self.config.get(section, option)
                return_string = return_string + " " + option + "=" + self.config.get(section, option)
        return return_string

# ========= get-functions ================

    ## @return get back the name of the logfile.
    def getLogFile(self):
        conf_value  = self.config.get("main", "logfile")
        return todoList


    def getTasksSettingsFile(self):
        try:
            conf_value  = self.config.get("main", "tasks_settings_file")
        except:
            self.config.set("main", "tasks_settings_file",  os.path.abspath(os.path.expanduser("~/taskssettings.moldau")))
            conf_value  =  os.path.abspath(os.path.expanduser("~/taskssettings.moldau"))
        return conf_value


# =============== set-functions =====================


    def setTasksSettingsFile(self, filename):
        self.config.set("main", "tasks_settings_file", filename)

        