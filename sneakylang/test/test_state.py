#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test context-sensitive Parser registry.
"""

from os import pardir
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))

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