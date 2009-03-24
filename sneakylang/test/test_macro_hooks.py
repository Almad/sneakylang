 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test macro hooks"""

# are not run

from unittest import main, TestCase

from module_test import *
from sneakylang.register import Register, RegisterMap
from sneakylang.macro_hook import MacroHook

class StrongMacroHook(MacroHook):
    macro = StrongMacro

    def pre_macro(self, stream, macro, builder):
        macro.arguments[0] = 'argument replaced by hook'
        return stream

    def post_macro(self, macro, builder):
        builder.insert(DummyNode(), 0, move_actual=False)


class TestMacroHook(TestCase):
    def testHookAddedToExistings(self):
        reg_map = RegisterMap({StrongMacro : Register()})
        reg_map.add_hooks([StrongMacroHook])

        self.assertEquals(set([StrongMacroHook]), reg_map.hooks[StrongMacro])

    def testHook(self):
        reg_map = RegisterMap({StrongMacro : Register()})
        reg_map.add_hooks([StrongMacroHook])

        s = '((silne "long argument"))'
        o = parse(s, reg_map, document_root = True)
        self.assertEquals(DummyNode, o.children[0].__class__)
        self.assertEquals(StrongNode, o.children[1].__class__)
        self.assertEquals("argument replaced by hook", o.children[1].children[0].content)

