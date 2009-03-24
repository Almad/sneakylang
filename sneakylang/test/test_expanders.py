 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Expanders """

from os import pardir
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))

from unittest import main,TestCase

from module_test import *

from sneakylang.macro import *
from sneakylang.err import *
from sneakylang.macro_caller import *
from sneakylang.register import Register, RegisterMap

#logging.basicConfig(level=logging.DEBUG)

class TestExpanding(TestCase):
    def setUp(self):
        self.register_map = RegisterMap({
            ParagraphMacro : Register([StrongMacro]),
            StrongMacro : Register([])
        })

        self.expander_map = {
             'docbook5' : {
             }
        }

    def testProperResolving(self):
        s = '((odstavec text odstavce))'
        o = parse(s, self.register_map, document_root=True)
        self.assertRaises(ExpanderError, lambda:expand(o, 'docbook5', self.expander_map))

if __name__ == "__main__":
    main()