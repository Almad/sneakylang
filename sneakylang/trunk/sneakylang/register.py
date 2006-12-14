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

from classregistry import registry, MasterRegistry, ClassRegistry
from expanders import Expander
from macro_caller import get_macro_name

class RegisterMap(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
#        self.macro_map = {}
        for k in self:
            self.__after_add(k)

    def __after_add(self, k):
        self[k].visit_register_map(self)
#        self.macro_map[k.macro.name] = self[k]

    def __setitem__(self, k, v):
        dict.__setitem__(self, k,v)
        self.__after_add(k)

class Register:
    def __init__(self, parsersList=None):
        # change to register_map,but now for backward compatibility
        self.register_map = None
        self.register_map = None
        self.parsers_start = {}
        self.parser_name_map = {}
        self.macro_map = {}
        self._emptyRegistry()
        if parsersList is not None:
            self.add_parsers(parsersList)

    def _emptyRegistry(self):
        MasterRegistry.registries[repr(self)] = ClassRegistry(repr(self))

    def _addParser(self, parser):
        if parser.start is None:
            return
        for regexp in parser.start:
            if not regexp.startswith('^') or not regexp.endswith('$'):
                raise ValueError, 'Regexp %s must start with ^ and ends with $ - others are not supported; should be, if You post an usecase' % regexp
            if self.parsers_start.has_key(regexp):
                raise ValueError, 'Register already contains parser %s starting on %s; %s nod added' % (self.parsers_start[regexp], regexp, parser)

            self.parser_name_map[parser.macro.name] = parser.__name__
            self.parsers_start[regexp] = parser
        registry(repr(self)).addClass(parser)

    def _addMacro(self, parser):
        if self.macro_map.has_key(parser.macro.name):
            raise ValueError, 'Macro %s already added under name %s' % (self.macro_map[parser.macro.name], parser.macro.name)
        self.macro_map[parser.macro.name] = parser.macro

    def add_parsers(self, parsersList):
        for p in parsersList:
            self.add(p)

    def add(self, parser):
        self._addParser(parser)
        self._addMacro(parser)

    def visit_register_map(self, map):
        self.register_map = map

    def get_parser(self, regexp):

        # should be better then has_key as mostly we will not raise exception
        try:
            return self.parsers_start[regexp]
        except KeyError:
            raise ValueError, 'No Parser in register starting with %s' % regexp

    def get_macro(self, name):
        try:
            return self.macro_map[name]
        except KeyError:
            raise ValueError, 'No macro parser registered under name %s in registry' % name

    def _most_matching(self, matching):
        most = None
        length = 0
        for m in matching:
            if len(m.string[m.start():m.end()]) > length:
                most = m
                length = len(m.string[m.start():m.end()])
        if most is None:
            return (None, None)
        return (self.parsers_start[''.join([most.re.pattern, '$'])], m.string[m.start():m.end()])

    def resolve_parser_macro(self, stream, map):
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

    def resolve_parser(self, stream):
        """ Resolve parser from my register_map in stream.
        Return properly initialized parser or None
        """
        if self.register_map is None:
            logging.info('''Trying to use Register without RegisterMap being set''')
        matching = [compile(p[:-1]).match(stream) for p in self.parsers_start if compile(p[:-1]).match(stream)]
        if len(matching) == 0:
            return None
        parser, chunk = self._most_matching(matching)
        if parser is None or chunk is None:
            return None
        return parser(stream, self, chunk, self.register_map)

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
