 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Macros and related things"""

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

from module_test import *

from sneakylang.macro import *
from sneakylang.macro_caller import *
from sneakylang.register import Register, RegisterMap
from sneakylang.treebuilder import TreeBuilder

#logging.basicConfig(level=logging.DEBUG)

class TestMacro(TestCase):
    def setUp(self):
        self.reg = Register([DummyMacro])
        self.reg_map = RegisterMap({DummyMacro : Register()})

    def testDefaultArgumentParsing(self):
        macro = DummyMacro(self.reg_map, TreeBuilder())
        macro.parse_argument_string(u"arg arg2")
        self.assertEquals(macro.arguments, [u'arg', u'arg2'])

if __name__ == "__main__":
    main()