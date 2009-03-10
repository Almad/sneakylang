# -*- coding: utf-8 -*-

""" Expanders for nodes
"""

from cgi import escape
from err import *

__all__ = ['Expander', 'TextNodeExpander', 'expand']

class Expander:
    def expand(self, node, format, node_map):
        pass

class TextNodeExpander(Expander):
    def expand(self, node, *args, **kwargs):
        return escape(node.content)

def expand(node_list, format, node_map):
    if type(node_list) != type([]):
        node_list = [node_list]
    try:
        return u''.join([node_map[format][node.__class__]().expand(node, format, node_map) for node in node_list])
    except KeyError:
        if not node_map.has_key(format):
            raise ExpanderError("Format not supported")
        if not node_map[format].has_key(node.__class__):
            raise ExpanderError("Expander for class %s not found" % repr(node.__class__))
        # no known cause, propagate original exception
        raise
