#! /usr/bin/env python
# -*- coding: utf-8 -*-


##
#    Copyright (C) 2011  Olaf Radicke
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


## Object-Typ for handling tasks.
class TaskTyp:


    ## The ID of a Task.
    ID = ""

    ## What typ of todo it is. "bash_command" or "replacement"
    #bash_command is do a bash command.
    #replacement is replace a old file with a new file.
    TodoTyp = "bash_command"

    ## The Bash command, to do.
    BashCommand = ""

    ## The file name which we would like remove.
    OldFile = ""

    ## The file name which we over write the old file.
    NewFile = ""

    ## Stop before execute task if "True"
    StopBefore = "False"

    ## Stop after execute task if "True"
    StopAfter = "False"

    ## A depiction of this task.
    Depiction = ""

    ##  It is "True" if skip this stap. Or "False".
    SkipStap = "False"


    # Constructor
#    def __init__(self):





