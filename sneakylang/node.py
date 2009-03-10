# -*- coding: utf-8 -*-

"""
Representation of nodes in Document
"""

from expanders import *

__all__ = ['Node', 'TextNode']

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.actual_text_content = None # actual TextNode to fill data in
        self.last_added_child = None

    def add_child(self, node, position=None):
        """ Add child or replace one at given position """
        # It's Python, we use implicit interfaces - isinstance considered harmful
#        if not isinstance(node, Node):
#            raise ValueError, 'Child of node must be instance of Node'

        if isinstance(node, TextNode):
            if self.actual_text_content is not None:
                raise ValueError, 'Adding a text node, but one is alread present'
            self.actual_text_content = node
        else:
            self.actual_text_content = None
        if position is None:
            if self.last_added_child:
                self.children.insert(self.children.index(self.last_added_child)+1, node)
            else:
                self.children.append(node)
        else:
            self.children[position] = node
        # visit node as parent
        node.parent = self
        self.last_added_child = node

    def insert_child(self, node, index):
        """ Insert child on given position """
        if isinstance(node, TextNode):
            if self.actual_text_content is not None:
                raise ValueError, 'Adding a text node, but one is alread present'
            self.actual_text_content = node
        else:
            self.actual_text_content = None
        self.children.insert(index, node)
        # visit node as parent
        node.parent = self
        self.last_added_child = node

    def expand(self, format):
        for child in self.childs:
            child.expand(format)

        if self.text_content is not None:
            if not self.expanders.has_key(format):
                raise NotImplementedError, "Macro %s does not support transformation to %s" % (self.name, format)
            self.expanders[format].expand(self.text_content)

class TextNode(Node):
    """ Special Node holding text.
    Begins when unresolved text discovered, ends when
    begin/end of any macro.
    Could not have any children.
    """
    def  __init__(self, content=u'', *args, **kwargs):
        self.content = content
        Node.__init__(self, *args, **kwargs)

    def add_char(self, char):
        self.content = u''.join([self.content, unicode(char)])

#    def __str__(self):
#        return str(self.content)