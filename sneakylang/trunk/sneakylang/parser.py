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

from classregistry import registry

class Parser(object):
    """ All parsers should derivate from this class """
    start = []
    macro = None
    name = None # should be same as macro.name

    def __init__(self, stream, register, chunk, map):
        """ Parse is taking activity in DOM dom because of chunk resolved """
        self.chunk = chunk
        self.register = register
        self.registerMap = map
        self.args = None
        self.init()
        self.stream = stream[len(chunk):]

    def init(self):
        """ Something to do after init? ,) """
        pass

    def beginParse(self):
        """ Begin parsing, set up needed things, determine whether to append
        stream to chunk or mark chunk as node_start
        """
        pass

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.args)

    def resolveContent(self):
        """ Resolve end of macro and (if needed) mark content as self.args """

    def checkValidity(self):
        return True

    def parse(self):
        self.beginParse()
        self.checkValidity()
        self.resolveContent()
        self.domTree = self.callMacro()
        return self.domTree

def _getTextNode(stream, register, registerMap, forceFirstChar=False):
    tn = TextNode()

    if forceFirstChar is True:
        tn.content = ''.join([tn.content, stream[0:1]])
        stream = stream[1:]

    while register.resolve_parser(stream, registerMap) is None:
        if len(stream) == 0:
            break
        tn.content = ''.join([tn.content, stream[0:1]])
        stream = stream[1:]
    return (tn, stream)

def parse(stream, registerMap, register=None):
    if register is None:
        register = Register([p for p in registerMap])
    nodes = []
    while len(stream) > 0:
        parser = register.resolve_parser(stream, registerMap)
        if parser is not None:
            logging.debug('Resolved parser %s' % parser)
            try:
                res = parser.parse()
                logging.debug('Appending %s' % res)
                nodes.append(res)
                stream = parser.stream
            except ParserRollback:
                node, stream = _getTextNode(stream, register, registerMap, True)
                nodes.append(node)
        else:
            logging.debug('Not resolved, adding TextNode')
            node, stream = _getTextNode(stream, register, registerMap)
            nodes.append(node)
    return nodes