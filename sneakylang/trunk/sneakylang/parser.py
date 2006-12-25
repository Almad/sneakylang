# -*- coding: utf-8 -*-

""" Parser transforming input stream to DOM
"""

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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

from err import ParserRollback

import macro
from node import TextNode
from register import Register
from macro_caller import expand_macro_from_stream

from classregistry import registry

class Parser(object):
    """ All parsers should derivate from this class """
    start = []
    macro = None

    def __init__(self, stream, parent_parser, chunk, register_map, register=None):
        """ Parse is taking activity in DOM dom because of chunk resolved """
        self.chunk = chunk
        self.parent_parser = parent_parser
        self.register_map = register_map
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

    def call_macro(self):
        """ Do proper call to related macro(s) """
        return self.macro.argument_call(self.argument_string, macro_instance=self.macro(self, self.register_map))

    def resolve_content(self):
        """ Resolve end of macro and (if needed) mark content as self.args """

    def check_validity(self):
        return True

    def parse(self):
        self.begin_parse()
        self.check_validity()
        self.resolve_content()
        self.dom_tree = self.call_macro()
        return self.dom_tree

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

    while register.resolve_parser(stream) is None:
        if len(stream) == 0:
            break
        tn.content = ''.join([tn.content, stream[0:1]])
        stream = stream[1:]
    return (tn, stream)

def parse(stream, register_map, register=None):
    if register is None:
        register = Register([p for p in register_map])
        register.visit_register_map(register_map)
    opened_text_node = None
    nodes = []
    while len(stream) > 0:
        parser = register.resolve_parser(stream)
        if parser is not None:
            logging.debug('Resolved parser %s' % parser)
            try:
                res = parser.parse()
                logging.debug('Appending %s' % res)
                nodes.append(res)
                stream = parser.stream
                opened_text_node = None
            except ParserRollback:
                logging.debug('Catched ParseRollback, forcing text char')
                node, stream = _get_text_node(stream, register, register_map, True, opened_text_node=opened_text_node)
                if opened_text_node is None:
                    nodes.append(node)
                opened_text_node=node
        else:
            # Is macro not in macro syntax?
            macro = register.resolve_parser_macro(stream, register_map)
            if macro is not None:
                # macro resolved, expand&add
                logging.debug('Macro %s resolved' % macro)
                macro_nodes, result_stream = expand_macro_from_stream(stream, register, register_map)
                logging.debug('Appending %s' % macro_nodes)
                nodes.append(macro_nodes)
                stream = result_stream
                opened_text_node = None
            else:
                logging.debug('Parser is None (not resolved), adding TextNode.')
                node, stream = _get_text_node(stream, register, register_map, opened_text_node=opened_text_node)
                if opened_text_node is None:
                    nodes.append(node)
                opened_text_node=node
    return nodes
