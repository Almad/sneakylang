# -*- coding: utf-8 -*-

""" Macros available in Czechtile by defualt.
Expected to b
"""

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
###

from err import *
import node
from register import Register

class Macro:
    """ All macros should derive from this class """
    name = None # define macro name
    help = """<this macro haven't specified usage example>"""
    parsersAllowed = None

    def __init__(self, register, registerMap):
        self.register = register
        self.registerMap = registerMap

    def expand(self, *args, **kwargs):
        """ Macro with arguments resolved; macro should expand themselves to Nodes and append to DOM """
        raise NotImplementedError


class Document(Macro):
    name = 'document'
    help = '<this macro should never be used>'

    def expand(self, text):
        from parser import DomParser
        p = DomParser(text, None, None)
        return p.parse(text)