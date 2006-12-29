#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from sneakylang.err import ParserRollback
from sneakylang.macro import Macro
from sneakylang.node import Node, TextNode
from sneakylang.parser import *
from sneakylang.register import Register, RegisterMap
from sneakylang.expanders import Expander, expand, TextNodeExpander


register_map = RegisterMap({
    ParagraphMacro : Register([StrongMacro], parsers_list),
    StrongMacro : Register(parsers=parsers_list)
})

node_map = {
     'docbook5' : {
         ParagraphNode : ParagraphDocbookExpand,
         TextNode : TextNodeExpander
     }
}
### End of definition


class TestParsing(TestCase):

    def testSimplestParaWithoutEnd(self):
        s = '''\n\nParagraph'''
        o = parse(s, register_map, parsers=parsers_list)
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph')

    def testSimplestParaWithEnd(self):
        s = '''\n\nParagraph\n\n'''
        o = parse(s, register_map, parsers=parsers_list)
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph')

    def testSimplestParaWithNoStrong(self):
        s = '''\n\nParagraph "" not strong, sorry ,)'''
        o = parse(s, register_map, parsers=parsers_list)
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph "" not strong, sorry ,)')

    def testParaWithStrong(self):
        s = '''\n\nParagraph ""strong""'''
        o = parse(s, register_map, parsers=parsers_list)
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0].__class__, ParagraphNode)
        self.assertEquals(len(o[0].children), 2)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph ')
        self.assertEquals(isinstance(o[0].children[1], StrongNode), True)
        self.assertEquals(isinstance(o[0].children[1].children[0], TextNode), True)
        self.assertEquals(o[0].children[1].children[0].content, 'strong')

class TestExpand(TestCase):
    def testExpandFromTree(self):
        p = ParagraphNode()
        tn = TextNode()
        tn.content = 'content'
        p.children.append(tn)
        self.assertEquals(expand(p, 'docbook5', node_map), '<para>content</para>')

    def testExpandFromTreeWithEntitiesEnabled(self):
        p = ParagraphNode()
        tn = TextNode()
        tn.content = '<b>not bold</b>'
        p.children.append(tn)
        self.assertEquals(expand(p, 'docbook5', node_map), '<para>&lt;b&gt;not bold&lt;/b&gt;</para>')

if __name__ == "__main__":
    main()