#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Negation
"""

from os import pardir
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))

from unittest import main, TestCase

from module_test import *

from sneakylang import parse, RegisterMap

#logging.basicConfig(level=logging.DEBUG)

NEGATION_CHAR = "!"

class TestNegation(TestCase):
    def setUp(self):
        self.register_map = RegisterMap({
            ParagraphMacro : Register([StrongMacro]),
            StrongMacro : Register()
        })

        self.expanderMap = {
             'docbook5' : {
                 ParagraphNode : ParagraphDocbookExpand,
                 TextNode : TextNodeExpander
             }
        }

    def testNegateMacroSyntax(self):
        s = NEGATION_CHAR+'((odstavec text odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, TextNode)
        self.assertEquals(o.children[0].content, '((odstavec text odstavce))')

    def testNegateMacroSyntaxWithTwoNegationsChars(self):
        s = 2*NEGATION_CHAR+'((odstavec text !odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, TextNode)
        self.assertEquals(o.children[0].content, NEGATION_CHAR+'((odstavec text !odstavce))')
    
    def testNegateParserSyntax(self):
        s = NEGATION_CHAR+'""strong""'
        o = parse(s, self.register_map, parsers=parsers_list, document_root=True)
        self.assertEquals(len(o.children), 1)
        self.assertEquals(o.children[0].__class__, TextNode)
        self.assertEquals(o.children[0].content, '""strong""')

if __name__ == "__main__":
    main()