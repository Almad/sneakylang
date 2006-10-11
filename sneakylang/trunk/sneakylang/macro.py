# -*- coding: utf-8 -*-

""" Macros available in Czechtile by defualt.
Expected to b
"""

###
#Czechtile: WikiHezkyCesky [http://projects.almad.net/czechtile]
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

class Macro:
    """ All macros should derive from this class """
    name = None # define macro name
    help = """<this macro haven't specified usage example>"""

    def expand(self, *args, **kwargs):
        """ Macro with arguments resolved; macro should expand themselves to Nodes and append to DOM """
        raise NotImplementedError


class Heading(Macro):
    name = 'nadpis'
    help = '((nadpis 1 Nadpis první úrovně)) ((nadpis 2 Nadpis druhé úrovně))'

    def _getHeading(self):
        n = node.Heading()
        t = TextNode()
        t.content = ''.join([''.join([word, ' ']) for word in args])
        n.append(t)
        return n

    def expand(self, dom, level, content):
        s = Section()
        s.append(self._getHeading())
        return s

class Strong(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

class Paragraph(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'
    macrosAllowed = [Strong]

    def expand(self, level, content):
        from parser import DomParser
        p = Paragraph()
        par = DomParser(register=self.macrosAllowed())
        p.append()
        return p

class Document(Macro):
    name = 'document'
    help = '<this macro should never be used>'
    macrosAllowed = [Heading, Paragraph]

    def expand(self, text):
        from parser import DomParser
        p = DomParser(text, None, None)
        return p.parse(text)