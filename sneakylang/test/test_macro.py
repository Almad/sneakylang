 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Macros and related things"""

from os import pardir
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))

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