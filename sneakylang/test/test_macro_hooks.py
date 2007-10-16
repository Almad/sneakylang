 #!/usr/bin/env python
# -*- coding: utf-8 -*-

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
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

""" Test macro hooks"""


from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import re

from unittest import main,TestCase

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

if __name__ == "__main__":
    main()