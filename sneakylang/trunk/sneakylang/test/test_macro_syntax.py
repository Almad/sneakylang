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
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main,TestCase
from module_test import *

#logging.basicConfig(level=logging.DEBUG)

from sneakylang import parse, RegisterMap, DocumentParser

class TestSimpleResolving(TestCase):
    def setUp(self):
        self.registerMap = RegisterMap({
            Paragraph : Register([Strong]),
            Strong : Register([]),
            DocumentParser : Register([Paragraph])
        })
        
        self.expanderMap = {
             'docbook5' : {
                 ParagraphNode : ParagraphDocbookExpand,
                 TextNode : TextNodeExpander,
                 Strong : StrongDocbookExpander
             }
        }
    
    def testProperResolving(self):
        s = '((odstavec text odstavce))'
        o = parse(s, self.registerMap)
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0].__class__, ParagraphNode)
        self.assertEquals(o[0].children[0].__class__, TextNode)
        self.assertEquals(o[0].children[0].content, 'text odstavce')
        # nefunguje, nutne udelat parsovani vnorenych maker
#        s = '((odstavec ((silne silny)) text odstavce))'
#        o = parse(s, self.registerMap)
#        self.assertEquals(len(o), 1)
#        self.assertEquals(o[0].__class__, ParagraphNode)
#        self.assertEquals(o[0].children[0].__class__, Strong)
#        self.assertEquals(o[0].children[0].children[0].__class__, TextNode)
#        self.assertEquals(o[0].children[0].children[0].content, 'silny')
#        self.assertEquals(o[0].children[1].__class__, TextNode)
#        self.assertEquals(o[0].children[1].content, ' text odstavce')
        

if __name__ == "__main__":
    main()