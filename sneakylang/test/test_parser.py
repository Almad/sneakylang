#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Parsers """

# is not run

from unittest import main,TestCase

from module_test import *

from sneakylang.parser import *
from sneakylang.register import Register, RegisterMap
from sneakylang import *

#logging.basicConfig(level=logging.DEBUG)

class TestParser(TestCase):

    def setUp(self):
        self.p = DummyParser('', None, '####', Register([DummyMacro]))

    def testMacroResolving(self):
        self.assertEquals(self.p.get_macro(TreeBuilder(), None)[0].__class__, DummyMacro)

class TestParserCapabilities(TestCase):

    def testParserTransform(self):
        register_map = RegisterMap({DummyMacro: Register([])})
        res = parse('####',register_map, parsers=[DummyParser])
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0].__class__, DummyNode)

    def testUnbreakedTextNodeProcessing(self):
        txt = '= jakoby nadpis\n= jakoby druhy nadpis'
        res = parse(txt, RegisterMap({NadpisMacro:Register()}), document_root=True)

        self.assertEquals(1, len(res.children))
        self.assertEquals(txt, res.children[0].content)

