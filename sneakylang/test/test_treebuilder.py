#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test context-sensitive Parser registry.
"""

from os import pardir
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))

from unittest import main, TestCase

#logging.basicConfig(level=logging.DEBUG)

from module_test import *
from sneakylang import *
from sneakylang.document import DocumentNode
from sneakylang.treebuilder import *

class DummyClass:
    def visit(self, *args, **kwargs):
        pass

class TestSupportedMethods(TestCase):
    def setUp(self):
        self.builder = TreeBuilder()

    def testBuildingForbiddenWithoutRoot(self):
        n2 = DummyNode()
        self.assertRaises(ValueError, lambda:self.builder.append(n2))

    def testNodeAppending(self):
        n1 = DummyNode()
        n2 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(self.builder.actual_node, n1)
        self.builder.append(n2, move_actual=True)
        self.assertEquals(self.builder.actual_node, n2)
        self.assertEquals(self.builder.actual_node.parent, n1)
        self.assertEquals(n2, n1.children[0])

    def testNodeInserting(self):
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(self.builder.actual_node, n1)
        self.builder.append(n2, move_actual=True)
        self.assertEquals(self.builder.actual_node, n2)
        self.assertEquals(self.builder.actual_node.parent, n1)
        self.assertEquals(n2, n1.children[0])
        self.builder.move_up()
        self.builder.insert(n3, 0)
        self.assertEquals([n3, n2], n1.children)

    def testLastAddedChildRemembering(self):
        ###FIXME: Refactor this to Node test
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        n4 = DummyNode()

        self.builder.set_root(n1)
        self.builder.append(n2, move_actual=True)
        self.builder.move_up()
        self.builder.insert(n3, 0, move_actual=False)
        self.assertEquals([n3, n2], n1.children)
        self.builder.append(n4)
        self.assertEquals([n3, n4, n2], n1.children)
        self.assertEquals(n4, n1.last_added_child)


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

    def testTreeBuilding(self):
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        n4 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(n1, self.builder.actual_node)
        self.builder.add_child(n2, move_actual=True)
        self.assertEquals(n2, self.builder.actual_node)
        self.builder.add_child(n3, False)
        self.assertEquals(n2, self.builder.actual_node)
        self.builder.append(n4, False)
        self.assertEquals(n2, self.builder.actual_node)

        self.assertEquals(n1, self.builder.root)
        self.assertEquals(n2, n1.children[0])
        self.assertEquals(n3, n2.children[0])
        self.assertEquals(n4, n2.children[1])

    def testSettingActualNodeByInstance(self):
        # first build some tree
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        n4 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(n1, self.builder.actual_node)
        self.builder.add_child(n2, move_actual=True)
        self.assertEquals(n2, self.builder.actual_node)
        self.builder.add_child(n3, False)
        self.assertEquals(n2, self.builder.actual_node)
        self.builder.append(n4, False)
        self.assertEquals(n2, self.builder.actual_node)

        self.builder.set_actual_node(n4)
        self.assertEquals(n4, self.builder.actual_node)

        self.assertRaises(ValueError, lambda:self.builder.set_actual_node(DummyNode()))

    def testListAdding(self):
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        n4 = DummyNode()
        n5 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(n1, self.builder.actual_node)

        self.builder.add_childs([n2, n3], move_actual=False)
        self.assertEquals(n1, self.builder.actual_node)
        self.assertEquals(n1, self.builder.root)
        self.assertEquals(n2, n1.children[0])
        self.assertEquals(n3, n1.children[1])
        self.assertEquals(n3, n1.last_added_child)

        self.builder.add_childs([n4, n5], True)
        self.assertEquals(n1, self.builder.root)
        self.assertEquals(n4, n1.children[2])
        self.assertEquals(n5, n1.children[3])
        self.assertEquals(n5, self.builder.actual_node)

    def testNodeReplacing(self):
        n1 = DummyNode()
        n2 = DummyNode()
        n3 = DummyNode()
        n4 = DummyNode()
        self.builder.set_root(n1)
        self.assertEquals(n1, self.builder.actual_node)

        self.builder.add_childs([n2, n3], True)
        self.builder.replace(n4)
        self.assertEquals(n4, self.builder.actual_node)
        self.builder.move_up()
        self.assertEquals([n2,n4], self.builder.actual_node.children)
        self.builder.set_actual_node(n1)
        self.builder.replace(n4)
        self.assertEquals(n4, self.builder.root)


class TestBuilderCalledByMacro(TestCase):
    def setUp(self):
        self.builder = TreeBuilder()

    def testCallingBuilder(self):
        s = '((silne test))'
        state = DummyClass()
        tree = parse(s, RegisterMap({StrongVistingMacro : Register()}), state=state, builder=self.builder, document_root=True)
        self.assertEquals(DocumentNode, tree.__class__)

if __name__ == "__main__":
    main()