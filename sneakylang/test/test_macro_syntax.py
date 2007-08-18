#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test macro syntax, now being build-in into main parser """

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
import logging
import re

from unittest import main,TestCase
from module_test import *

#logging.basicConfig(level=logging.DEBUG)

from sneakylang import parse, RegisterMap, Document

class TestArgumentParsing(TestCase):
    def testParsingShortArgument(self):
        s = '((onearg test))'
        o = parse(s, RegisterMap({OneArgumentMacro : Register()}), document_root = True)
        self.assertEquals(DummyNode, o.children[0].__class__)
        self.assertEquals("test", o.children[0].children[0].content)

    def testParsingLongArgument(self):
        s = '((onearg "long argument"))'
        o = parse(s, RegisterMap({OneArgumentMacro : Register()}), document_root = True)
        self.assertEquals(DummyNode, o.children[0].__class__)
        self.assertEquals("long argument", o.children[0].children[0].content)

class TestSimpleResolving(TestCase):
    def setUp(self):
        self.register_map = RegisterMap({
            ParagraphMacro : Register([StrongMacro]),
            StrongMacro : Register([]),
            Document : Register([ParagraphMacro])
        })

        self.expanderMap = {
             'docbook5' : {
                 ParagraphNode : ParagraphDocbookExpand,
                 TextNode : TextNodeExpander
             }
        }

    def testProperResolving(self):
        s = '((odstavec text odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(o.children[0].children[0].__class__, TextNode)
        self.assertEquals(o.children[0].children[0].content, 'text odstavce')

    def testBadCall(self):
        s = '((odstavec))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, TextNode)
        self.assertEquals(o.children[0].content, '((odstavec))')

class TestNestedMacroSyntax(TestCase):
    def setUp(self):
        self.register_map = RegisterMap({
            ParagraphMacro : Register([StrongMacro]),
            StrongMacro : Register([]),
            Document : Register([ParagraphMacro])
        })

        self.expanderMap = {
             'docbook5' : {
                 ParagraphNode : ParagraphDocbookExpand,
                 TextNode : TextNodeExpander
             }
        }

    def testProperNested(self):
        s = '((odstavec ((silne silny)) text odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(o.children[0].children[0].__class__, Strong)
        self.assertEquals(o.children[0].children[0].children[0].__class__, TextNode)
        self.assertEquals(o.children[0].children[0].children[0].content, 'silny')
        self.assertEquals(o.children[0].children[1].__class__, TextNode)
        self.assertEquals(o.children[0].children[1].content, ' text odstavce')

