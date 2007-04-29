# -*- coding: utf-8 -*-

""" Parser transforming input stream to DOM
"""

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/c~/projects/sneakylang/sneakylang/testzechtile/wiki/Contributors
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
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
###

import logging

from err import ParserRollback, MacroCallError

import macro
from node import TextNode
from register import Register
from macro_caller import expand_macro_from_stream

class Parser(object):
    """ All parsers should derivate from this class """
    start = []
    macro = None

    def __init__(self, stream, parent_parser, chunk, register):
        """ Parse is taking activity in DOM dom because of chunk resolved """
        self.chunk = chunk
        self.parent_parser = parent_parser
        self.argument_string = ''
        self.init()
        self.stream = stream[len(chunk):]
        self._register = register

    def init(self):
        """ Something to do after init? ,) """
        pass

    def begin_parse(self):
        """ Begin parsing, set up needed things, determine whether to append
        stream to chunk or mark chunk as node_start
        """
        pass

    def _get_macro(self):
        return self.macro.argument_call(self.argument_string, self.register)

    def resolve_argument_string(self):
        """ Resolve transform content to argument string which would be used if calling macro by macro syntax """

    def get_macro(self):
        """ Return properly istantiazed macro and new stream """
        self.begin_parse()
        self.resolve_argument_string()
        return (self._get_macro(), self.stream)

    def parse(self):
        macro, self.stream = self.get_macro()
        return macro.expand()
#        self.dom_tree = self.call_macro()
#        return self.dom_tree

    def get_register(self):
        if self._register is not None:
            return self._register
        else:
            return self.register_map[self.__class__]

    register = property(fget=get_register)


def _get_text_node(stream, register, register_map, force_first_char=False, opened_text_node=None):
    if opened_text_node is None:
        tn = TextNode()
    else:
        tn = opened_text_node

    if force_first_char is True:
        tn.content = ''.join([tn.content, stream[0:1]])
        stream = stream[1:]

    while True:
        try:
            res = register.resolve_macro(stream)
        except (ParserRollback, MacroCallError):
            pass
        else:
            if res != (None, None):
                break
        if len(stream) == 0:
            break
        tn.content = ''.join([tn.content, stream[0:1]])
        stream = stream[1:]
    return (tn, stream)

#TODO: Reduce this as constant
NEGATION="!"

def parse(stream, register_map, register=None, parsers=None, state=None):
    if register is None:
        register = Register([p for p in register_map])
        register.visit_register_map(register_map)
        if parsers is not None:
            register.add_parsers(parsers)
    opened_text_node = None
    negation_buffer = None
    nodes = []
    while len(stream) > 0:
        try:
            macro, stream_new = register.resolve_macro(stream)
            if macro is not None and stream_new is not None:
                logging.debug('Resolved macro %s' % macro)
                res = macro.expand(state=state)
                logging.debug('Appending %s' % res)
                nodes.append(res)
                stream = stream_new
                opened_text_node = None
            else:
                # parser not resolved, add text node
                node, stream = _get_text_node(stream, register, register_map, opened_text_node=opened_text_node)
                if opened_text_node is None:
                    nodes.append(node)
                opened_text_node=node
        except (ParserRollback, MacroCallError):
            #badly resolved macro
            logging.debug('Catched ParseRollback, forcing text char')
            node, stream = _get_text_node(stream, register, register_map, True, opened_text_node=opened_text_node)
            if opened_text_node is None:
                nodes.append(node)
            opened_text_node=node
    return nodes
