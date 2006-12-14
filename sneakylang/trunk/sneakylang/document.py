# -*- coding: utf-8 -*-

""" Default document macro/nodes """

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/sneakylang/wiki/Contributors
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

import logging

from macro import Macro
from parser import Parser, parse
from node import Node

class Document(Macro):
    name = 'document'
    help = '<toto makro se nikdy nepouziva explicitne>'

    @classmethod
    def parse_argument_string(self, argument_string):
        return (argument_string,)
    
    def expand(self, content):
        doc = DocumentNode()
        logging.debug('Creating document node and parsing document')
        res = parse(content, self.register_map, self.register)
        for node in res:
            if node is not None:
                doc.add_child(node)
        return doc


class DocumentParser(Parser):
    start = None
    macro = Document

    def resolve_content(self):
        self.args = self.stream
        self.stream = ''

#    def call_macro(self):
#        """ Do proper call to related macro(s) """
#        return self.macro(self.register, self.register_map).expand(self.content, self.parser)

class DocumentNode(Node): pass