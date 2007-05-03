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

    def expand_to_nodes(self, *args, **kwargs):
        self.builder.append(DummyNode())

class DummyNode(Node):
    name = 'dummy node'

class DummyParser(Parser):
    start = ['(####)']
    macro = DummyMacro

class DummyParserTwo(Parser):
    start = ['(#####)']
    macro = DummyMacro

class NadpisMacro(Macro):
    name = 'nadpis'

    def expand_to_nodes(self, *args, **kwargs):
        return DummyNode()

# parser borrowed from czechtile
class Nadpis(Parser):
    start = ['(\n)?(=){1,5}(\ ){1}']
    macro = NadpisMacro

    def resolve_argument_string(self):
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
    def get_argument_list(self, argument_string):
        return [argument_string]

    def expand_to_nodes(self, content, **kwargs):
        self.builder.append(ParagraphNode())
        parse(content, self.register_map, self.register, builder=self.builder)
        self.builder.move_up()

class Paragraph(Parser):
    start = ['(\n){2}']
    macro = ParagraphMacro
    end = '(\n){2}'

    def resolve_argument_string(self):
        end = re.search(self.__class__.end, self.stream)
        if end:
            self.argument_string = self.stream[0:end.start()]
            self.chunk_end = self.stream[end.start():end.end()]
            self.stream = self.stream[end.end():]
        else:
            self.argument_string = self.stream
            self.stream = ''

class StrongNode(Node): pass

class StrongMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand_to_nodes(self, content, **kwargs):
        self.builder.append(StrongNode(), move_actual=True)
        parse(content, self.register_map, self.register, builder=self.builder)
        self.builder.move_up()

class StrongVistingMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand_to_nodes(self, content, *args, **kwargs):
        self.state.visit(self)
        self.builder.append(StrongNode())
        self.builder.append(TextNode(content=content), move_actual=False)
        self.builder.move_up()

class Strong(Parser):
    start = ['("){2}']
    macro = StrongMacro
    end = '("){2}'

    def resolve_argument_string(self):
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

parsers_list = [DummyParser, DummyParserTwo, Paragraph, Nadpis, Strong]
