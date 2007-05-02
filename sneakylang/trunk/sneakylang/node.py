# -*- coding: utf-8 -*-

""" Representation of nodes in Document
"""

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
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
    def __init__(self):
        self.parent = None
        self.children = []
        self.actual_text_content = None # actual TextNode to fill data in

    def add_child(self, node):
        # It's Python, we use implicit interfaces - isinstance considered harmful
#        if not isinstance(node, Node):
#            raise ValueError, 'Child of node must be instance of Node'
        if isinstance(node, TextNode):
            if self.actual_text_content is not None:
                raise ValueError, 'Adding a text node, but one is alread present'
            self.actual_text_content = node
        else:
            self.actual_text_content = None
        self.children.append(node)
        # visit node as parent
        node.parent = self

#    def add_text_content(self, stream):
#        if self.actual_text_content is None:
#            self.add_child(TextNode(parent=self, chunk=None))
#
#        self.actual_text_content.add_char(stream[0:1])
#        return stream[1:]

    def expand(self, format):
        for child in self.childs:
            child.expand(format)

        if self.text_content is not None:
            if not self.expanders.has_key(format):
                raise NotImplementedError, "Macro %s does not support transformation to %s" % (self.name, format)
            self.expanders[format].expand(self.text_content)
#    def __str__(self):
#        return ''.join(['['] + [str(child) for child in self.children] + [']'])

class TextNode(Node):
    """ Special Node holding text.
    Begins when unresolved text discovered, ends when
    begin/end of any macro.
    Could not have any children.
    """
    def  __init__(self, *args, **kwargs):
        self.content = ''
        Node.__init__(self, *args, **kwargs)

    def add_char(self, char):
        self.content = ''.join([self.content, str(char)])

#    def __str__(self):
#        return str(self.content)