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

#logging.basicConfig(level=logging.DEBUG)

from sneakylang.err import ParserRollback
from sneakylang.macro import Macro
from sneakylang.node import Node, TextNode
from sneakylang.parser import *
from sneakylang.register import Register
from sneakylang.expanders import Expander, expand, TextNodeExpander


### Define basic grammar
# This wiki have only paragraps (\n\n) and headings (=)

class ParagraphNode(Node): pass

class ParagraphMacro(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'
    parsersAllowed = ['Strong']

    def expand(self, content):
        p = ParagraphNode()
        logging.debug('Parsing paragraph content')
        nodes = parse(content, self.registerMap)
        logging.debug('Appedding result %s to paragraph' % nodes)
        for n in nodes:
            p.addChild(n)
        logging.debug('Expanding node %s' % p)
        return p

class Paragraph(Parser):
    start = ['^(\n){2}$']
    macro = ParagraphMacro
    end = '(\n){2}'

    def resolveContent(self):
        end = re.search(self.__class__.end, self.stream)
        if end:
            self.content = self.stream[0:end.start()]
            self.chunk_end = self.stream[end.start():end.end()]
            self.stream = self.stream[end.end():]
        else:
            self.content = self.stream
            self.stream = ''

    def callMacro(self):
        macro = self.__class__.macro(self.register, self.registerMap)
        return macro.expand(self.content)

class StrongNode(Node): pass

class StrongMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand(self, content):
        n = StrongNode()
        tn = TextNode()
        tn.content = content
        n.addChild(tn)
        return n

class Strong(Parser):
    start = ['^("){2}$']
    macro = StrongMacro
    end = '("){2}'

    def resolveContent(self):
        s = self.stream
        end = re.search(self.__class__.end, s)
        if not end:
            logging.debug('End %s of macro %s not found, rolling back' % (self.__class__.end, self))
            raise ParserRollback
        self.stream = s
        self.content = self.stream[0:end.start()]
        self.stream = self.stream[end.end():]

    def callMacro(self):
        macro = self.__class__.macro(self.register, self.registerMap)
        return macro.expand(self.content)

registerMap = {
    Paragraph : Register([Strong]),
    Strong : Register()
}

class ParagraphDocbookExpand(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<para>'] + [expand(child, format, node_map) for child in self.node.children] + ['</para>'])

class StrongDocbookExpander(Expander):
    def expand(self, node, format, node_map):
        pass

expanderMap = {
     'docbook5' : {
         Paragraph : ParagraphDocbookExpand,
         TextNode : TextNodeExpander,
         Strong : StrongDocbookExpander
     }
}
### End of definition


class TestParsing(TestCase):
    def setUp(self):
        self.reg = Register()
        self.reg.add(Paragraph)
        self.reg.add(Strong)

    def testSimplestPara(self):
        s = '''\n\nParagraph'''
        o = parse(s, registerMap)
        self.assertEquals(len(o), 1)
        self.assertEquals(isinstance(o[0], ParagraphNode), True)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph')

    def testSimplestParaWithEnd(self):
        s = '''\n\nParagraph\n\n'''
        o = parse(s, registerMap)
        self.assertEquals(len(o), 1)
        self.assertEquals(isinstance(o[0], ParagraphNode), True)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph')

    def testSimplestParaWithNoStrong(self):
        s = '''\n\nParagraph "" not strong, sorry ,)'''
        o = parse(s, registerMap)
        self.assertEquals(len(o), 1)
        self.assertEquals(isinstance(o[0], ParagraphNode), True)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph ')
        self.assertEquals(o[0].children[1].content, '"" not strong, sorry ,)')

    def testParaWithStrong(self):
        s = '''\n\nParagraph ""strong""'''
        o = parse(s, registerMap)
        self.assertEquals(len(o), 1)
        self.assertEquals(isinstance(o[0], ParagraphNode), True)
        self.assertEquals(len(o[0].children), 2)
        self.assertEquals(isinstance(o[0].children[0], TextNode), True)
        self.assertEquals(o[0].children[0].content, 'Paragraph ')
        self.assertEquals(isinstance(o[0].children[1], StrongNode), True)
        self.assertEquals(isinstance(o[0].children[1].children[0], TextNode), True)
        self.assertEquals(o[0].children[1].children[0].content, 'strong')

class TestExpand:

    def testExpandFromTree(self):
        p = ParagraphNode()
        p.children[0] = TextNode().content = 'content'
        self.assertEquals(expand(p), '<para>content</para>')

if __name__ == "__main__":
    main()