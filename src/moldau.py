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


import sys
from MoldauConf import MoldauConf
from zsettings import ZSettings
from zdirector import ZDirector
from optparse import OptionParser
from GUI import MainWindow
from PyQt4 import QtGui, QtCore


## @file zauberlehrling.py
# @author Olaf Radicke<radicke@atix.de>

moldauConf   = MoldauConf()
progSettings = ZSettings()
progDirector = ZDirector(progSettings)


##############  callbacks #######################

## Is calling the function gotoTodo of ZDirector.
def gotoTodo(option, opt, value, parser):
    #ifGoTo = True
    GotoStap = value
    print("ifGoTo... ")
    progDirector.gotoTodo(GotoStap)
    sys.exit(0)

def initConf(option, opt, value,  parser):
    progSettings.generateNewConfigFile()
    sys.exit(0)

def checkPath(option, opt,  value, parser):
    #ifCheckPath = True
    print("ifCheckPath...")
    progSettings.checkPathes()
    sys.exit(0)

def setConfFile(option, opt,  value, parser):
    progSettings.setConfFile(value)

def goQtGUI(option, opt,  value, parser):
    #ifQtGUI = True
    print("ifQtGUI... ")
    # star GUI....
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
    sys.exit(0)

## parse command line options with OptionParser
#  very important point: allway set 'type="string" in the "add_option()"'. Python
# is not Type safety!! So is'it type not set, the programm can crash by runtime.
def initArgPars():

    parser = OptionParser()
    parser.add_option("-g",
                      "--goto=",
                      action="callback",
                      callback=gotoTodo,
                      dest="sprungziel",
                      type="string",
                      help="Das Programm setzt an der genannten Stell ein.")
                      
    help_text = "Generiert im aktuellen Verzeichnis eine standard Konfiguration mit Namen." \
       + progSettings.configFile + "'."
    parser.add_option("-i",
                      "--initconf",
                      action="callback",
                      callback=initConf,
                      help=help_text)
                      
    help_text = "Prueft ob alle Dateipfade in der config gefunden werden koennen.'"
    parser.add_option("-c",
                      "--checkpath",
                      action="callback",
                      callback=checkPath,
                      help=help_text)


    help_text = "QU-GUI starten."
    parser.add_option("-x",
                      "--qt-gui",
                      action="callback",
                      callback=goQtGUI,
                      help=help_text)     
                      
    help_text = "Eine bestimmte Konfigurationsdatei mitgeben." 
    parser.add_option("-f",
                      "--conffile",
                      action="callback",
                      callback=setConfFile,
                      help=help_text)


                      
    (options, args) = parser.parse_args()



## The main function startin at first an parsing the comand-line.
def main():

    initArgPars()

    progDirector.start()
    sys.exit(0)

main()
