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

from err import ParserRollback

import macro
from node import TextNode

from classregistry import registry

#class ResolverParser(Parser):
#    """ Special 'main parser'.
#    Resolving other parsers and return them. If unsuccessfull,
#    creating TextNodes and appending them to tree """
#
#    def __init__(self, stream):
#        self.stream = stream
#
#    def parse(self, register=None):
#        pass

class Parser(object):
    """ All parsers should derivate from this class """
    start = []
    macro = None
    name = None # should be same as macro.name

    def __init__(self, stream, register, chunk):
        """ Parse is taking activity in DOM dom because of chunk resolved """
        self.chunk = chunk
        if register is None:
            #TODO: some default register
            self.register = None
        else:
            self.register = register
        self.args = None
        self.init()
        self.stream = stream

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
        return self.macro().expand(self.args)

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

class Document(Parser):
    start = None
    macro = macro.Document

    def __init__(self, stream, register=None, chunk=None):
        DomParser.__init__(self, stream, register, chunk)

    def resolveContent(self):
        self.args = self.stream


def parse(stream, register):
    nodes = []
    p = register.resolve_parser(stream)
    if p is not None:
        stream = stream[len(p.chunk):]
        n = p.parse()
        nodes.append(n)
    else:
        tn = TextNode()
        while register.resolve_parser(stream) is None:
            if len(stream) == 0:
                break
            tn.content = ''.join([tn.content, stream[0:1]])
            stream = stream[1:]
        nodes.append(tn)
    if len(stream) > 0:
        nodes.append(parse(stream, register))
    return nodes