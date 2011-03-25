#!/usr/bin/python
# -*- coding: utf-8 -*-


 ###########################################################################
 #   Copyright (C) 2010 by Olaf Radicke <briefkasten@olaf-radicke.de>      #
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

## @file TaskTyp.py
# @author Olaf Radicke<briefkasten@olaf-radicke.de>


## the class handling and represent a item in a log.
class TaskLogItem:

    ## the name of task.
    step_id = ""

    ## the time stamp of execute
    timestamp = ""

    ## type of stap
    step_type = ""

    ## what the stap was do.
    done = ""

    ## what the command is giving back.
    result = ""

    logNote = ""
    