#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test context-sensitive Parser registry.
"""

from unittest import TestCase

#logging.basicConfig(level=logging.DEBUG)

from sneakylang.register import *

from sneakylang.macro import Macro
from sneakylang.parser import Parser
from sneakylang.treebuilder import TreeBuilder

class DummyMacro(Macro):
    name = 'dummy_macro'

class DummyParser(Parser):
    start = ['(#){4}']
    macro = DummyMacro

class DummyParserWithTwoPossibleStarts(Parser):
    start = ['^(####)$', '^(||||)$']
    macro = DummyMacro

class AnotherDummyMacro(Macro):
    name = 'another_dummy_macro'

class AnotherDummyParser(Parser):
    start = ['--']
    macro = AnotherDummyMacro

class NationalParser(Parser):
    start = ['(\w){3}']
    macro = AnotherDummyMacro

class NotAllowedParserCreatingCollisionWithMacro(Parser):
    # already in register
    start = ['^(\(){2}$']

class NotAllowedParserHavingBadRegexp(Parser):
    # already in register
    start = ['(\(){2}$']

class NotAllowedParserHavingBadRegexp2(Parser):
    # already in register
    start = ['^(\(){2}']

class TestParserRegister(TestCase):
    def testProperRegexpRetrieving(self):
        reg = ParserRegister([DummyParser])
        self.assertEquals(DummyParser, reg.get_parser('(#){4}'))

        r2 = ParserRegister([DummyParserWithTwoPossibleStarts])
        self.assertEquals(DummyParserWithTwoPossibleStarts, r2.get_parser('^(####)$'))
        self.assertEquals(DummyParserWithTwoPossibleStarts, r2.get_parser('^(||||)$'))

        self.assertRaises(ValueError, lambda:r2.get_parser('some regexp that do not exists'))

    def testRetrievingFromStream(self):
        reg = ParserRegister([DummyParser])
        self.assertEquals(reg.resolve_parser('####', Register()).__class__, DummyParser)

    def testResolvingOfOverlappingMacrosFromStream(self):
        class DummyMacroTwo(Macro):
            name = 'dummy_macro_two'
        class DummyParserTwo(Parser):
            start = ['^(#####)$']
            macro = DummyMacroTwo

        reg = ParserRegister([DummyParser, DummyParserTwo])
        self.assertEquals(reg.resolve_parser('#### 123', Register()).__class__, DummyParser)
        self.assertEquals(reg.resolve_parser('#####', Register()).__class__, DummyParserTwo)

    def testResolvingOfOverlappingMacrosFromStreamGivenInOtherOrder(self):
        class DummyMacroTwo(Macro):
            name = 'dummy_macro_two'
        class DummyParserTwo(Parser):
            start = ['^(#####)$']
            macro = DummyMacroTwo

        reg = ParserRegister([DummyParserTwo, DummyParser])
        self.assertEquals(reg.resolve_parser('#### 123', Register()).__class__, DummyParser)
        self.assertEquals(reg.resolve_parser('#####', Register()).__class__, DummyParserTwo)

    def testProperResolvingWithNationalChars(self):
        reg = ParserRegister([NationalParser])
        self.assertEquals(reg.resolve_parser('žšť', Register()).__class__, NationalParser)

    def testAcceptingUnicodeString(self):
        reg = ParserRegister([NationalParser])
        self.assertEquals(reg.resolve_parser(u'žšť', Register()).__class__, NationalParser)

class TestRegister(TestCase):

    def setUp(self):
        self.r = Register()
        self.builder = TreeBuilder()

    def testMacroHolding(self):
        self.r.add(DummyMacro)
        self.assertEquals(DummyMacro, self.r.get_macro('dummy_macro'))

        self.r.add_parser(AnotherDummyParser)
        self.assertEquals(False, AnotherDummyParser.start[0] in self.r.parser_register.parser_start)

        self.assertEquals((None,None), self.r.resolve_macro('####', self.builder))
        self.r.add_parser(DummyParser)
        self.assertEquals(DummyMacro, self.r.resolve_macro('####', self.builder)[0].__class__)

        self.r.add_parser(AnotherDummyParser)
        self.assertEquals((None,None), self.r.resolve_macro('--', self.builder))
        self.r.add(AnotherDummyMacro)
        self.assertEquals((None,None), self.r.resolve_macro('--', self.builder))
        self.r.add_parser(AnotherDummyParser)
        self.assertEquals(AnotherDummyMacro, self.r.resolve_macro('--', self.builder)[0].__class__)

    def testEasyParserAdding(self):
        reg = Register([DummyMacro, AnotherDummyMacro], [DummyParser, AnotherDummyParser])
        self.assertEquals(DummyMacro, reg.resolve_macro('####', self.builder)[0].__class__)
        self.assertEquals(AnotherDummyMacro, reg.resolve_macro('--', self.builder)[0].__class__)

    def testNotAddingParserWhichHasNotMacroAlreadyInRegister(self):
        reg = Register([DummyMacro], [DummyParser])
        self.assertEquals(False, AnotherDummyParser.start[0] in reg.parser_register.parser_start)
        self.assertEquals((None, None), reg.resolve_macro('--', self.builder))

    def testNotAddingParserWhichHasNotMacroAlreadyInRegisterWithEasyAdding(self):
        reg = Register([DummyMacro], [DummyParser, AnotherDummyParser])
        self.assertEquals(False, AnotherDummyParser.start[0] in reg.parser_register.parser_start)
        self.assertEquals((None, None), reg.resolve_macro('--', self.builder))


class TestRegisterMap(TestCase):
    def testProperVisit(self):
        map = RegisterMap()
        map[DummyParser] = Register([])
        self.assertEquals(map[DummyParser].register_map, map)
        self.assertEquals(repr(map[DummyParser].register_map), repr(map))
        map = RegisterMap({DummyParser : Register([])})
        self.assertEquals(map[DummyParser].register_map, map)
        self.assertEquals(repr(map[DummyParser].register_map), repr(map))
