#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

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



class MainClass():

    def Start(self):
        print "Start..."
        
    def Stop(self):
        print "...Stop"
    

print "l�uft..."
mc = MainClass()
mc.Start()
mc.Stop()
