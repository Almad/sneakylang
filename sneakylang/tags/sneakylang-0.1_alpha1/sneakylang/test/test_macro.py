#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Macros and related things"""

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

from module_test import *

from sneakylang.macro import *
from sneakylang.macro_caller import *
from sneakylang.register import Register

#logging.basicConfig(level=logging.DEBUG)

class TestMacroCaller(TestCase):
    def setUp(self):
        self.reg = Register([DummyParser])
        
    def testDefaultArgumentParsing(self):
        args = Macro.parse_argument_string("arg arg2")
        self.assertEquals(args, ['arg', 'arg2'])
    
    def testContentResolving(self):
        self.assertEquals('arg arg', get_content('arg arg))adf'))
        self.assertEquals('dummy_macro', get_content('dummy_macro))'))
        self.assertEquals(None, get_content('arg arg'))
        self.assertEquals(None, get_content('arg arg \n))'))
    
    def testResolveName(self):
        self.assertEquals(('dummy_macro', None), resolve_macro_name('dummy_macro'))
        self.assertEquals(('dummy_macro', 'arg arg'), resolve_macro_name('dummy_macro arg arg'))
        
    def testResolvingFromRegister(self):
        self.assertEquals('dummy_macro', resolve_name_from_register('dummy_macro', self.reg))
    
    def testResolvingNameFromMacro(self):
        self.assertEquals('dummy_macro', get_macro_name('((dummy_macro))', self.reg))
        self.assertEquals('dummy_macro', get_macro_name('((dummy_macro argument argument))', self.reg))
        self.assertEquals(None, get_macro_name('((dummy_macro argument argument haha', self.reg))
        self.assertEquals(None, get_macro_name('((dummy_macro argument argument \n)) Multiline not allowed', self.reg))

    def testMacroExpanding(self):
        self.assertEquals(DummyNode, call_macro(DummyMacro, None, Register([DummyParser])).__class__)
        self.assertEquals(DummyNode, expand_macro_from_stream('((dummy_macro))', self.reg, Register([DummyParser]))[0].__class__)
    
    def testEnlosedArgumentParsing(self):
        #FIXME: Do proper argument parsing, now disabled
#        args = parse_arguments('"this is one arg"')
#        self.assertEquals(args, ['this is one arg'])
        pass
        
    # TODO: Proper argument parsing, see macro.parse_arguments docstring

if __name__ == "__main__":
    main()