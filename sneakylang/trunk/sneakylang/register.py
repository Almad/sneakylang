# -*- coding: utf-8 -*-

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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

import logging
from re import compile

from expanders import Expander
from macro_caller import get_macro_name, expand_macro_from_stream

class RegisterMap(dict):
    """ Register map is dictionary holding macro : register_with_allowed_macros pair """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        for k in self:
            self.__after_add(k)

    def __after_add(self, k):
        self[k].visit_register_map(self)

    def __setitem__(self, k, v):
        dict.__setitem__(self, k,v)
        self.__after_add(k)

class ParserRegister:
    """ Parser register is holding parsers (aka 'alternative syntaxes') allowed to use for parsing.
    ParserRegister is also responsible for resolving those alternative syntaxes in stream """

    def __init__(self, parsers=None):
        self.parser_start = {}
        self.parser_start_compiled = {}

        if parsers is not None:
            for parser in parsers:
                self.add(parser)

    def add(self, parser):
        if parser.start is not None:
            for start in parser.start:
                self.parser_start[start] = parser
                self.parser_start_compiled[compile(''.join(['^', start]))] = parser

    def get_parser(self, regexp):
        try:
            return self.parser_start[regexp]
        except KeyError:
            raise ValueError, 'No Parser in register starting with %s' % regexp

    def _most_matching(self, matching):
        """ Return most matching parser and chunk on which it's resolved """
        most = None
        length = 0
        for m in matching:
            if len(m.string[m.start():m.end()]) > length:
                most = m
                length = len(m.string[m.start():m.end()])
        if most is None:
            return (None, None)
        return (self.parser_start[most.re.pattern[1:]], most.string[most.start():most.end()])

    def resolve_parser(self, stream, register):
        """ Resolve parser stream.
        Return properly initialized parser or None
        """
        matching = [parser_start.match(stream) for parser_start in self.parser_start_compiled if parser_start.match(stream)]
        if len(matching) == 0:
            return None
        parser, chunk = self._most_matching(matching)
        if parser is None or chunk is None:
            return None
        return parser(stream, self, chunk, register)

class Register:
    def __init__(self, macro_list=None, parsers=None):
        self.register_map = None
        self.macro_map = {}

        self.parser_register = ParserRegister()

        if macro_list is not None:
            self.add_macros(macro_list)

        if parsers is not None:
            self.add_parsers(parsers)

    def add_macro(self, macro):
        if self.macro_map.has_key(macro.name):
            raise ValueError, 'Macro %s already added under name %s' % (self.macro_map[macro.name], macro.name)
        self.macro_map[macro.name] = macro

    def add_macros(self, macro_list):
        for p in macro_list:
            self.add(p)

    def add(self, macro):
        """ Backward-compatibility symlink, use add_macro instead """
        self.add_macro(macro)

    def add_parsers(self, parsers):
        for parser in parsers:
            self.add_parser(parser)

    def add_parser(self, parser):
        if parser.macro.name in self.macro_map:
            self.parser_register.add(parser)

    def visit_register_map(self, register_map):
        self.register_map = register_map

    def get_macro(self, name):
        try:
            return self.macro_map[name]
        except KeyError:
            raise ValueError, 'No macro parser registered under name %s in registry' % name

    def resolve_parser_macro(self, stream):
        """ Try resolving parser in macro syntax.
        Return properly initialized parser or None
        """
        logging.debug('Trying to resolve macro in stream')
        try:
            return self.macro_map[get_macro_name(stream, self)]
        except KeyError:
            logging.debug('Macro name %s not in my macro_map' % get_macro_name(stream,self))
            return None
        else:
            raise ValueError, 'Unexpected exception, please report this as bug'

    def resolve_macro(self, stream):
        parser = self.parser_register.resolve_parser(stream, self)
        if parser is not None:
            macro, stream_new = parser.get_macro()
            return (macro, stream_new)

        # resolve in macro syntax
        macro = self.resolve_parser_macro(stream)
        if macro is not None:
            return expand_macro_from_stream(stream, self)

        return (None, None)

class ExpanderRegister:
    def __init__(self, expander_map):
        self.expander_map = {}
        for k in expander_map:
            if not isinstance(expander_map[k], Expander):
                raise ValueError, '%s must be instance of Expander' % expander_map[k]
            self.expander_map[k] = expander_map[k]

    def get(self, node, format='xhtml11'):
        try:
            return self.expander_map[format][node]
        except KeyError:
            raise ValueError, 'Expander for format %s for node %s not in registry' % (format, node)
