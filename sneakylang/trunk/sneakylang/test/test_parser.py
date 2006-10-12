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

from unittest import main,TestCase

logging.basicConfig(level=logging.DEBUG)

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import *
from sneakylang.register import Register

class DummyMacro(Macro):
    name = 'dummy_macro'

    def expand(self, *args):
        return DummyNode(None)

class DummyNode(Node):
    name = 'dummy node'

class DummyParser(Parser):
    parser_start = ['^(####)$']
    macro = DummyMacro
    name = 'dummy_macro' # remove when bug #2 will be solved

class DummyParserTwo(Parser):
    parser_start = ['^(#####)$']
    macro = DummyMacro
    name = 'dummy_macro' # remove when bug #2 will be solved

class TestParserCapabilities(TestCase):

    def testSameName(self):
        self.assertEquals(DummyParser.name, DummyMacro.name)

    def testParserTransform(self):
        r = Register()
        r.add(DummyParser)
        res = parse('####',r)
        self.assertEquals(len(res), 1)
        self.assertEquals(isinstance(parse('####',r)[0], DummyNode), True)



if __name__ == "__main__":
    main()