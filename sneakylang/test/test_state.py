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

from unittest import main,TestCase

#logging.basicConfig(level=logging.DEBUG)

from module_test import StrongVistingMacro
from sneakylang import *

class VisitedStateClass:
    def __init__(self):
        self.visited = 0

    def visit(self, macro):
        self.visited += 1

class TestStateArgument(TestCase):
    def testVisit(self):
        s = '((silne test))'
        state = VisitedStateClass()
        tree = parse(s, RegisterMap({StrongVistingMacro : Register()}), state=state, document_root=True)
        self.assertEquals(state.visited, 1)




if __name__ == "__main__":
    main()