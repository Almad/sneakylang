#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for commons shared by tests """

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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

import re

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import *
from sneakylang.register import Register

from sneakylang.err import ParserRollback
from sneakylang.macro import Macro
from sneakylang.node import Node, TextNode
from sneakylang.parser import *
from sneakylang.register import Register
from sneakylang.expanders import Expander, expand, TextNodeExpander

class DummyMacro(Macro):
    name = 'dummy_macro'

    def expand(self, *args):
        return DummyNode(None)

class DummyNode(Node):
    name = 'dummy node'

class DummyParser(Parser):
    start = ['^(####)$']
    macro = DummyMacro

class DummyParserTwo(Parser):
    start = ['^(#####)$']
    macro = DummyMacro

# parser borrowed from czechtile
class Nadpis(Parser):
    start = ['^(\n)?(=){1,5}(\ ){1}$']
    macro = DummyMacro

    def resolve_content(self):
        endPattern = self.chunk[:-1]
        if endPattern.startswith('\n'):
            endPattern = endPattern[1:]
        # chunk is \n={n}[whitespace],
        # end is [whitespace]={n}\n
        endMatch = re.search(''.join([' ', endPattern, '\n']), self.stream)
        if not endMatch:
            raise ParserRollback
        self.level = len(endPattern)
        self.argument_string = self.stream[0:endMatch.start()]
        # end()-1 because we won't eat trailing newline
        self.chunk_end = self.stream[endMatch.start():endMatch.end()-1]
        self.stream = self.stream[endMatch.end()-1:]

    def call_macro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.register_map).expand(self.level, self.argument_string)

### Define basic grammar
# This wiki have only paragraps (\n\n) and headings (=)

class ParagraphNode(Node): pass

class ParagraphMacro(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'
    parsersAllowed = ['Strong']

    @classmethod
    def parse_argument_string(self, argument_string):
        return [argument_string]

    def expand(self, content):
        p = ParagraphNode()
        logging.debug('Parsing paragraph content')
        nodes = parse(content, self.register_map, self.register)
        logging.debug('Appedding result %s to paragraph' % nodes)
        for n in nodes:
            p.add_child(n)
        logging.debug('Expanding node %s' % p)
        return p

class Paragraph(Parser):
    start = ['^(\n){2}$']
    macro = ParagraphMacro
    end = '(\n){2}'

    def resolve_content(self):
        end = re.search(self.__class__.end, self.stream)
        if end:
            self.argument_string = self.stream[0:end.start()]
            self.chunk_end = self.stream[end.start():end.end()]
            self.stream = self.stream[end.end():]
        else:
            self.argument_string = self.stream
            self.stream = ''

#    def call_macro(self):
#        return self.__class__.macro.argument_call(self.argument_string, register=self.register)

class StrongNode(Node): pass

class StrongMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand(self, content):
        n = StrongNode()
        tn = TextNode()
        tn.content = content
        n.add_child(tn)
        return n

class Strong(Parser):
    start = ['^("){2}$']
    macro = StrongMacro
    end = '("){2}'

    def resolve_content(self):
        s = self.stream
        end = re.search(self.__class__.end, s)
        if not end:
            logging.debug('End %s of macro %s not found, rolling back' % (self.__class__.end, self))
            raise ParserRollback
        self.stream = s
        self.argument_string = self.stream[0:end.start()]
        self.stream = self.stream[end.end():]

class ParagraphDocbookExpand(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<para>'] + [expand(child, format, node_map) for child in node.children] + ['</para>'])

class StrongDocbookExpander(Expander):
    def expand(self, node, format, node_map):
        pass
