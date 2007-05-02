#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test context-sensitive Parser registry.
"""

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

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging

from unittest import main,TestCase, TestSuite

#logging.basicConfig(level=logging.DEBUG)

from module_test import *
from sneakylang import *
from sneakylang.treebuilder import *

class DummyClass:
    def visit(self, *args, **kwargs):
        pass

class TestSupportedMethods(TestCase):
    def setUp(self):
        self.builder = TreeBuilder()

    def testTreeAppendingWithoutRoot(self):
        self.assertRaises(ValueError, lambda:self.builder.append(DummyNode()))

    def testNodeAdding(self):
        n1 = DummyNode()
        n2 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(self.builder.actual_node, n1)
        self.builder.append(n2, move_actual=True)
        self.assertEquals(self.builder.actual_node, n2)
        self.assertEquals(self.builder.actual_node.parent, n1)
        self.assertEquals(n2, n1.children[0])

    def testTreeTraversing(self):
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(n1, self.builder.actual_node)
        self.builder.append(n2, move_actual=True)
        self.builder.move_up()
        self.assertEquals(n1, self.builder.actual_node)
        self.builder.append(n3, move_actual=False)
        self.assertEquals(n1, self.builder.actual_node)

class TestBuilderCalledByMacro(TestCase):
    def setUp(self):
        self.builder = TreeBuilder()

    def testCallingBuilder(self):
        s = '((silne test))'
        state = DummyClass()
        tree = parse(s, RegisterMap({StrongVistingMacro : Register()}), state=state, builder=self.builder)

if __name__ == "__main__":
    main()