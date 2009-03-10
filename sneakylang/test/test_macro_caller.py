#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test macro caller functions """

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

import os
import sys
sys.path.insert(0, os.path.join(os.pardir, os.pardir))
import logging
import re

from unittest import main,TestCase
from module_test import *

from sneakylang.macro_caller import *
from sneakylang.treebuilder import TreeBuilder

#logging.basicConfig(level=logging.DEBUG)

class TestArgumentParsing(TestCase):
    def testEmptyArgument(self):
        self.assertEquals(None, parse_macro_arguments(u""))

    def testSingleWord(self):
        self.assertEquals([u"test"], parse_macro_arguments(u"test"))

    def testWhitespaceSeparatedWords(self):
        self.assertEquals([u"testing", u"args"], parse_macro_arguments(u"testing args"))

    def testLongArgumentWithinQuotation(self):
        self.assertEquals([u"testing arg"], parse_macro_arguments(u'"testing arg"'))

    def testLongArgumentWithinQuotationWithSeparateWord(self):
        self.assertEquals([u"testing arg", u"argument"], parse_macro_arguments(u'"testing arg" argument'))

    def testCombinationOfQuotedAndSeparatedWords(self):
        self.assertEquals([u"arg", u"harg", u"testing arg", u"argument"], parse_macro_arguments(u'arg "harg" "testing arg" argument'))

    def testKeywordArgument(self):
        self.assertEquals(([], {'argument' : 'testing arg'}), parse_macro_arguments(u'argument="testing arg"', return_kwargs=True))

    def testKeywordMustBeNamed(self):
        self.assertEquals((["blah", '="testing arg"'], {}), parse_macro_arguments(u'blah ="testing arg"', return_kwargs=True))

class TestHelperFunctions(TestCase):
    def test_strip_long_argument_chunk(self):
        self.assertEquals((u" aaa", u'"testing chunk"'), strip_long_argument_chunk(u'"testing chunk" aaa', u''))
        self.assertEquals((u'"testing chunkaaa', ''), strip_long_argument_chunk(u'"testing chunkaaa', u''))

    def test_move_chars(self):
        self.assertEquals(('ba', 'a'), move_chars("a", "aba", ""))
        self.assertRaises(ValueError, lambda:move_chars("a", "zzz", ""))

    def test_nested_macro_chunk(self):
        self.assertEquals("((yess))", get_nested_macro_chunk("((yess))"))


class TestMacroCaller(TestCase):
    def setUp(self):
        self.reg = Register([DummyMacro])

    def testContentResolving(self):
        self.assertEquals('arg arg', get_content('arg arg))adf'))
        self.assertEquals('dummy_macro', get_content('dummy_macro))'))
        self.assertEquals(None, get_content('arg arg'))
        self.assertEquals(None, get_content('arg arg \n))'))

    def testResolveName(self):
        self.assertEquals(('dummy_macro', None), resolve_macro_name('dummy_macro'))
        self.assertEquals(('dummy_macro', 'arg arg'), resolve_macro_name('dummy_macro arg arg'))
#
    def testResolvingFromRegister(self):
        self.assertEquals('dummy_macro', resolve_name_from_register('dummy_macro', self.reg))

    def testResolvingNameFromMacro(self):
        self.assertEquals('dummy_macro', get_macro_name('((dummy_macro))', self.reg))
        self.assertEquals('dummy_macro', get_macro_name('((dummy_macro argument argument))', self.reg))
        self.assertEquals(None, get_macro_name('((dummy_macro argument argument haha', self.reg))
        self.assertEquals(None, get_macro_name('((dummy_macro argument argument \n)) Multiline not allowed', self.reg))

    def testMacroExpanding(self):
        builder = TreeBuilder(root=DummyNode())
        call_macro(DummyMacro, '', Register([DummyMacro]), builder, None)
        self.assertEquals(DummyNode, builder.root.children[0].__class__)
        res = expand_macro_from_stream('((dummy_macro))', self.reg, TreeBuilder, None)
        self.assertEquals(res[0].__class__, DummyMacro)
        self.assertEquals(res[1], '')

if __name__ == "__main__":
    main()