#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Parsers
"""

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

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main,TestCase

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import *
from sneakylang.register import Register

#logging.basicConfig(level=logging.DEBUG)

class DummyMacro(Macro):
    name = 'dummy_macro'

    def expand(self, *args):
        return DummyNode(None)

class DummyNode(Node):
    name = 'dummy node'

class DummyParser(Parser):
    start = ['^(####)$']
    macro = DummyMacro
    name = 'dummy_macro' # remove when bug #2 will be solved

class DummyParserTwo(Parser):
    start = ['^(#####)$']
    macro = DummyMacro
    name = 'dummy_macro' # remove when bug #2 will be solved

# parser borrowed from czechtile
class Nadpis(Parser):
    start = ['^(\n)?(=){1,5}(\ ){1}$']
    macro = DummyMacro
    name = 'dummy_macro'

    def resolveContent(self):
        endPattern = self.chunk[:-1]
        if endPattern.startswith('\n'):
            endPattern = endPattern[1:]
        # chunk is \n={n}[whitespace],
        # end is [whitespace]={n}\n
        endMatch = re.search(''.join([' ', endPattern, '\n']), self.stream)
        if not endMatch:
            raise ParserRollback
        self.level = len(endPattern)
        self.content = self.stream[0:endMatch.start()]
        # end()-1 because we won't eat trailing newline
        self.chunk_end = self.stream[endMatch.start():endMatch.end()-1]
        self.stream = self.stream[endMatch.end()-1:]

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.level, self.content)


class TestParserCapabilities(TestCase):

    def testSameName(self):
        self.assertEquals(DummyParser.name, DummyMacro.name)

    def testParserTransform(self):
        map = {DummyParser : Register()}
        res = parse('####',map)
        self.assertEquals(len(res), 1)
        self.assertEquals(isinstance(res[0], DummyNode), True)
    
    def testUnbreakedTextNodeProcessing(self):
        txt = '= jakoby nadpis\n= jakoby druhy nadpis'
        res = parse(txt, {Nadpis:Register()})
        self.assertEquals(1, len(res))
        self.assertEquals(txt, res[0].content)

if __name__ == "__main__":
    main()