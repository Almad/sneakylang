# -*- coding: utf-8 -*-

""" Parser transforming input stream to DOM
"""

###
#Czechtile: WikiHezkyCesky [http://projects.almad.net/czechtile]
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/czechtile/wiki/Contributors
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

from classregistry import registry

class ParserRegister:
    macros_start = {}
    macros_end = {}

    def add(self, node):
        #TODO: add ((macro_name arg)) syntax
        for i in node.node_start:
            self.macros_start[i] = node
        for i in set(node.node_end):
            self.macros_end[i] = node

    def _matchingChunk(self, regexp, stream, no=1):
        if re.compile(regexp).match(stream[0:no]):
            return stream[0:no]
        return self._matchingChunk(regexp, stream, no=no+1)


    def get_node(self, stream):
        """ Get nodes from stream.
        Return tuple(NodeClass,, chunk_of_stream_matching_start_pattern, rest_of_stream)
        """
        matching = []
        for i in self.macros_start:
            if not i.endswith('$') or not i.startswith('^'):
                raise ValueError, "Node's start and end regular expression pattern but be on limited characters, so it must start with ^ and end with $. Other types of regular expressions are not (yet?) supported."
            if re.compile(i[:-1]).match(stream):
                matching.append((self.macros_start[i],i))

        if len(matching) == 0:
            return None
        elif len(matching) == 1:
            ch = self._matchingChunk(matching[0][1], stream)
            return (matching[0][0], ch, stream[len(ch):])

        raise NotImplementedError

defaultParserRegister = MacroRegister()

class ParserGroup:
    """ Used as a "classifier"; when parser is specifying children, their should allow
    both Parser and ParserGroup """

class Parser:
    """ All parsers should derive from this class. """

    def __new__(cls):
        # add class to registry
        if not cls.__bases__ == (object,):
            registry('parser').addClass(cls)

class ResolverParser(Parser):
    """ Special 'main parser'.
    Resolving other parsers and return them. If unsuccessfull,
    creating TextNodes and appending them to tree """

    def __init__(self, stream):
        self.stream = stream

    def parse(self, register=defaultParserRegister): pass

class DomParser(Parser):

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
        self.parse()

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

class Document(DomParser):
    start = None
    macro = macro.Document

    def __init__(self, stream, register=None, chunk=None):
        DomParser.__init__(self, stream, register, chunk)

    def resolveContent(self):
        self.args = self.stream


class Heading(DomParser):
    # when is parser starting activity
    start = ['^(\n){1}(=)+(\ ){1}$']
    macro = macro.Heading

    def beginParse(self, stream):
        self.level = len(self.chunk[1:-1])

    def checkValidity(self, stream):
        if not re.match(''.join(['^(^\n)+(\ ', '='*self.level, '\n)']), stream):
            raise ParserRollback

    def callMacro(self, stream):
        content = stream[0:re.match(''.join(['(\ ', '='*self.level, '\n'])).end()]
        stream = stream[0:len(content)-1] #-1, we won't eat \n
        macro = Heading()
        macro.expand(self.dom, self.level, content)

class Paragraph(DomParser):
    start = ['^(\n){2}$']
    macro = macro.Paragraph

    def callMacro(self, stream):
        content = stream[0:re.match('(\n){2}').end()]
        stream = stream[0, len(content)-2]
        macro = Paragraph()
        macro.expand(self.dom, content)
