#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test macro syntax, now being build-in into main parser """

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
        self.assertEquals(u"test", o.children[0].children[0].content)

    def testParsingLongArgument(self):
        s = '((onearg "long argument"))'
        o = parse(s, RegisterMap({OneArgumentMacro : Register()}), document_root = True)
        self.assertEquals(DummyNode, o.children[0].__class__)
        self.assertEquals(u"long argument", o.children[0].children[0].content)

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
                 TextNode : TextNodeExpander,
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

    def testProperNested(self):
        s = '((odstavec ((silne silny)) text odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(o.children[0].children[0].__class__, StrongNode)
        self.assertEquals(o.children[0].children[0].children[0].__class__, TextNode)
        self.assertEquals(o.children[0].children[0].children[0].content, 'silny')
        self.assertEquals(o.children[0].children[1].__class__, TextNode)
        self.assertEquals(o.children[0].children[1].content, ' text odstavce')

    def testProperNestedQuoted(self):
        s = '((odstavec "silne silny)) text odstavce"))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, ParagraphNode)
        self.assertEquals(o.children[0].children[0].__class__, TextNode)
        self.assertEquals(o.children[0].children[0].content, 'silne silny)) text odstavce')

class TestKeywordMacroArguments(TestCase):
    def setUp(self):
        self.register_map = RegisterMap({
            PictureKeywordMacro : Register(),
            Document : Register([PictureKeywordMacro]),
        })

    def test_kwargs_resolved(self):
        s = '((picture http://pic.png title="My picture"))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(1, len(o.children))
        self.assertEquals(PictureNode, o.children[0].__class__)
        self.assertEquals(u"My picture", o.children[0].kwargs['title'])

