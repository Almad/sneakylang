# -*- coding: utf-8 -*-

""" Representation of nodes in Document
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

import re
import logging

from expanders import *

class Node:
    # if expand to desired format supported,
    # expander must be given
    expanders = {# -*- coding: utf-8 -*-

        'xhtlm11' : None,
        'docbook5' : None
    }

    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.actualTextContent = None # actual TextNode to fill data in

    def addChild(self, node):
        if not isinstance(node, Node):
            raise ValueError, 'Child of node must be instance of Node'
        if isinstance(node, TextNode):
            self.actualTextContent = node
        else:
            self.actualTextContent = None
        self.children.append(node)

    def addTextContent(self, stream):
        if self.actualTextContent is None:
            self.addChild(TextNode(parent=self, chunk=None))

        self.actualTextContent.addChar(stream[0:1])
        return stream[1:]

    def expand(self, format):
        for child in self.childs:
            child.expand(format)

        if self.textContent is not None:
            if not self.expanders.has_key(format):
                raise NotImplementedError, "Macro %s does not support transformation to %s" % (self.name, format)
            self.expanders[format].expand(self.textContent)

class TextNode(Node):
    """ Special Node holding text.
    Begins when unresolved text discovered, ends when
    begin/end of any macro.
    Could not have any children.
    """
    def  __init__(self, *args, **kwargs):
        self.content = ''
        Node.__init__(self, *args, **kwargs)

    def addChar(self, char):
        self.content = ''.join([self.content, str(char)])

###
# Default nodes used in default Czechtile transformation
###
### Perhaps split in separate module

class Document(Node):
    def __init__(self):
        Node.__init__(self, parent=False, chunk='')

class MacroHandler(Node):
    """ Very special one, actual macro executer """

###
# End of standard nodes
###
