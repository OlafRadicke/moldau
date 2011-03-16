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


import sys
import os.path
from MoldauConf import MoldauConf
from TasksSettings import TasksSettings
from zdirector import ZDirector
from optparse import OptionParser



## @file zauberlehrling.py
# @author Olaf Radicke<radicke@atix.de>


class Moldau:


##############  callbacks #######################

    ## Callback: Is calling the function goto todo stap.
    def gotoTodo(self, option, opt, value, parser):
        #ifGoTo = True
        GotoStap = value
        print("ifGoTo... ")
        moldauConf   = MoldauConf()
        tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())
        progDirector = ZDirector(tasksSettings)
        progDirector.gotoTodo(GotoStap)
        sys.exit(0)

    ## Callback: build a new configuration and a task-seting-file.
    def initConf(self, option, opt, value,  parser):
        print "Create... "
        moldauConf   = MoldauConf()
        print "\n... '" + moldauConf.configFile  + "'."
        moldauConf.generateNewConfigFile()
        tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())
        print "\n... " + tasksSettings.configFile + "'"
        tasksSettings.generateNewConfigFile()
        print "\n...done"
        sys.exit(0)

    ## Callback: Check the pathes in the task-seting-file.
    def checkPath(self, option, opt,  value, parser):
        #ifCheckPath = True
        print("ifCheckPath...")
        tasksSettings.checkPathes()
        sys.exit(0)

    ## Callback: Set the path of the task-seting-file.
    def setConfFile(self, option, opt,  value, parser):
        moldauConf   = MoldauConf()
        tasksSettings = TasksSettings(moldauConf.getTasksSettingsFile())
        tasksSettings.setConfFile(value)
        progDirector = ZDirector(tasksSettings)
        progDirector.start()

    ## Callback: Starting the GUI-Interface
    def goQtGUI(self, option, opt,  value, parser):
        import GUI
        print("ifQtGUI... ")
        # star GUI....
        GUI.startGUI()
        sys.exit(0)

    ## parse command line options with OptionParser
    #  very important point: allway set 'type="string" in the "add_option()"'. Python
    # is not Type safety!! So is'it type not set, the programm can crash by runtime.
    def initArgPars(self):

        parser = OptionParser()
        parser.add_option("-g",
                          "--goto=",
                          action="callback",
                          callback=self.gotoTodo,
                          dest="sprungziel",
                          type="string",
                          help="Das Programm setzt an der genannten Stell ein.")

        help_text = "Generiert Dateien mit standard Konfiguration."
        parser.add_option("-i",
                          "--initconf",
                          action="callback",
                          callback=self.initConf,
                          help=help_text)

        help_text = "Prueft ob alle Dateipfade in der config gefunden werden koennen.'"
        parser.add_option("-c",
                          "--checkpath",
                          action="callback",
                          callback=self.checkPath,
                          help=help_text)


        help_text = "QU-GUI starten."
        parser.add_option("-x",
                          "--qt-gui",
                          action="callback",
                          callback=self.goQtGUI,
                          help=help_text)

        help_text = "Eine bestimmte Konfigurationsdatei mitgeben."
        parser.add_option("-f",
                          "--conffile",
                          action="callback",
                          callback=self.setConfFile,
                          help=help_text)



        (options, args) = parser.parse_args()



## The main function startin at first an parsing the comand-line.
def main():

    print "dir: '" + os.path.abspath(os.path.expanduser("~/.test")) + "'"
    moldau = Moldau()
    moldau.initArgPars()
    sys.exit(0)

main()
