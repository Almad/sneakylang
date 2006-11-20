#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test context-sensitive Parser registry.
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

from sneakylang.register import *

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import Parser

from sneakylang.classregistry import registry

class DummyMacro(Macro):
    name = 'dummy_macro'

class DummyParser(Parser):
    start = ['^(####)$']
    macro = DummyMacro
    name = 'dummy_macro' # remove when bug #2 will be solved

class DummyParserWithTwoPossibleStarts(Parser):
    start = ['^(####)$', '^(||||)$']
    macro = DummyMacro
    name = 'dummy_ts_macro'

class NotAllowedParserCreatingCollisionWithMacro(Parser):
    # already in register
    start = ['^(\(){2}$']

class NotAllowedParserHavingBadRegexp(Parser):
    # already in register
    start = ['(\(){2}$']

class NotAllowedParserHavingBadRegexp2(Parser):
    # already in register
    start = ['^(\(){2}']

class TestDistinctHolders(TestCase):
    def testDistinctHoldersAndNoDuplicatesInOne(self):
        r1 = Register()
        r2 = Register()

        r1.add(DummyParser)
        self.assertRaises(ValueError, lambda:r1.add(DummyParser))
        self.assertRaises(ValueError, lambda:registry(repr(r1)).addClass(DummyParser))

        r2.add(DummyParser)
        self.assertRaises(ValueError, lambda:r2.add(DummyParser))
        self.assertRaises(ValueError, lambda:registry(repr(r2)).addClass(DummyParser))

class SimpleAddition(TestCase):
    def setUp(self):
        self.r = Register()

    def testAdd(self):
        self.r.add(DummyParser)
        self.assertEquals(self.r.parsers_start['^(####)$'], DummyParser)

    def testBadAdd(self):
        self.assertRaises(ValueError, lambda:self.r.add(NotAllowedParserHavingBadRegexp))
        self.assertRaises(ValueError, lambda:self.r.add(NotAllowedParserHavingBadRegexp2))

class TestRetrieving(TestCase):
    def setUp(self):
        self.r = Register()
        self.r.add(DummyParser)

        self.r2 = Register([DummyParser])

        self.map = {DummyParser:Register()}

    def testGet(self):
        self.assertEquals(DummyParser, self.r.get_parser('^(####)$'))

    def testBadGet(self):
        self.assertRaises(ValueError, lambda:self.r.get_parser('SomeBadRegullarExpressions'))

    def testGet(self):
        self.assertEquals(DummyMacro, self.r.get_macro('dummy_macro'))
        self.assertEquals(DummyMacro, self.r2.get_macro('dummy_macro'))

    def testResolver(self):
        self.assertEquals(isinstance(self.r.resolve_parser('####', self.map), DummyParser), True)

    def testResolverConflicting(self):

        class DummyMacroTwo(Macro):
            name = 'dummy_macro_two'
        class DummyParserTwo(Parser):
            start = ['^(#####)$']
            macro = DummyMacroTwo
            name = 'dummy_macro_two' # remove when bug #2 will be solved

        self.r.add(DummyParserTwo)
        self.map[DummyParserTwo] = Register()
        self.assertEquals(isinstance(self.r.resolve_parser('#### 123', self.map), DummyParser), True)
        self.assertEquals(isinstance(self.r.resolve_parser('#####', self.map), DummyParserTwo), True)

class TestInstanceCreating(TestCase):
    def testReg(self):
        r = Register([DummyParser])
        self.assertEquals(DummyParser, r.get_parser('^(####)$'))

        r2 = Register([DummyParserWithTwoPossibleStarts])
        self.assertEquals(DummyParserWithTwoPossibleStarts, r2.get_parser('^(####)$'))
        self.assertEquals(DummyParserWithTwoPossibleStarts, r2.get_parser('^(||||)$'))


if __name__ == "__main__":
    main()