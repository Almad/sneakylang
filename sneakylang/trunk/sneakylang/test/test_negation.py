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

from unittest import main,TestCase, TestSuite

from module_test import *
from sneakylang import parse, RegisterMap, Document

#logging.basicConfig(level=logging.DEBUG)

###TODO: Negation not in plan yet
#class TestParserNegation(TestCase):
#    def testNegateStrong(self):
#        pass
#
#class TestMacroNegation(TestCase):
#    def setUp(self):
#        self.register_map = RegisterMap({
#            ParagraphMacro : Register([StrongMacro]),
#            StrongMacro : Register([]),
#            Document : Register([ParagraphMacro])
#        })
#
#        self.expanderMap = {
#             'docbook5' : {
#                 ParagraphNode : ParagraphDocbookExpand,
#                 TextNode : TextNodeExpander             }
#        }
#
#    def testNegateStrong(self):
#        s = '!((odstavec text odstavce))'
#        o = parse(s, self.register_map)
#        self.assertEquals(len(o), 1)
#        self.assertEquals(o[0].__class__, ParagraphNode)
#        self.assertEquals(o[0].children[0].__class__, TextNode)
#        self.assertEquals(o[0].children[0].content, '((odstavec text odstavce))')

if __name__ == "__main__":
    main()