#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from module_test import *

#logging.basicConfig(level=logging.DEBUG)

# not run

from sneakylang.node import TextNode
from sneakylang.parser import parse
from sneakylang.register import Register, RegisterMap
from sneakylang.expanders import expand, TextNodeExpander


register_map = RegisterMap({
    ParagraphMacro : Register([StrongMacro], parsers_list),
})

node_map = {
     'docbook5' : {
         ParagraphNode : ParagraphDocbookExpand,
         TextNode : TextNodeExpander
     }
}
### End of definition


class TestSimpleWikiParsing(TestCase):

    def testSimplestParaWithoutEnd(self):
        s = '''\n\nParagraph'''
        o = parse(s, register_map, parsers=parsers_list, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o.children[0].children[0], TextNode), True)
        self.assertEquals(o.children[0].children[0].content, 'Paragraph')

    def testSimplestParaWithEnd(self):
        s = '''\n\nParagraph\n\n'''
        o = parse(s, register_map, parsers=parsers_list, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o.children[0].children[0], TextNode), True)
        self.assertEquals(o.children[0].children[0].content, 'Paragraph')

    def testSimplestParaWithNoStrong(self):
        s = '''\n\nParagraph "" not strong, sorry ,)'''
        o = parse(s, register_map, parsers=parsers_list, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(isinstance(o.children[0].children[0], TextNode), True)
        self.assertEquals(o.children[0].children[0].content, 'Paragraph "" not strong, sorry ,)')

    def testParaWithStrong(self):
        s = '''\n\nParagraph ""strong""'''
        o = parse(s, register_map, parsers=parsers_list, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(len(o.children[0].children), 2)
        self.assertEquals(isinstance(o.children[0].children[0], TextNode), True)
        self.assertEquals(o.children[0].children[0].content, 'Paragraph ')
        self.assertEquals(isinstance(o.children[0].children[1], StrongNode), True)
        self.assertEquals(isinstance(o.children[0].children[1].children[0], TextNode), True)
        self.assertEquals(o.children[0].children[1].children[0].content, 'strong')

class TestSimpleWikiExpand(TestCase):
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
