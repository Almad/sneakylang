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

def root_required(fn):
    """ Decorator for administrator authorization
    """
    def _innerWrapper(self, *args, **kwargs):
        if self.root is None:
            raise ValueError, "For this operation, root for treebuilder must be set"
        return fn(self, *args, **kwargs)
    return _innerWrapper


class TreeBuilder(object):
    def __init__(self, root=None):
        self.root = root
        # pointer to actual node
        self._actual_node = root

    @root_required
    def append(self, node, move_actual=True):
        if self._actual_node is None:
            self.tree.append(node)
        else:
            self._actual_node.add_child(node)
        if move_actual is True:
            self._actual_node = node

    @root_required
    def move_up(self):
        if self.actual_node.parent is None:
            raise ValueError, 'Cannot move up as there is no parent of current node'
        else:
            self._actual_node = self.actual_node.parent

    @root_required
    def add_child(self, node, move_actual=True):
        self._actual_node.add_child(node)
        if move_actual is True:
            self._actual_node = node

    @root_required
    def add_childs(self, nodes, move_actual=True):
        for node in nodes:
            self.add_child(node, False)
        if move_actual is True:
            self._actual_node = node

    def set_root(self, node):
        self.root = node
        self._actual_node = node

    def get_actual_node(self):
        return self._actual_node
    
    def get_node_from_children(self, node, node_list):
        if node in node_list:
            return node
        else:
            for n in node_list:
                return self.get_node_from_children(node, n.children)
    
    def set_actual_node(self, node):
        """ Traverse through node tree, find given node instance and set it as active node.
        If node is not found, raise ValueError """
        if not self.root is None and self.get_node_from_children(node, self.root.children) == node:
            self._actual_node = node
        else:
            raise ValueError, 'Node %s not found in tree' % node

    actual_node = property(fget=get_actual_node)