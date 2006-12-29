# -*- coding: utf-8 -*-

""" SneakyLang: Extensible WikiFramework """

__version__ = "0.2_alpha2"

###
# SneakyLang: Extensible WikiFramework
# Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/czechtile/wiki/Contributors
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

from err import *
from register import *
from expanders import *
from macro import *
from node import *
from parser import *
from document import *

def parse_start(stream, register_map):
    parser = DocumentParser(stream, register_map[document.DocumentParser], '', register_map)
    documentNode = parser.parse()
    return documentNode
