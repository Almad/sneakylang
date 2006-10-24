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

from re import compile

from classregistry import registry, MasterRegistry, ClassRegistry
from expanders import Expander

class Register:
    def __init__(self, parsersList=None):
        self.parsers_start = {}
        self.parser_name_map = {}
        self.macro_map = {}
        self._emptyRegistry()
        if parsersList is not None:
            self.addParsers(parsersList)

    def _emptyRegistry(self):
        MasterRegistry.registries[repr(self)] = ClassRegistry(repr(self))

    def _addParser(self, parser):
        for regexp in parser.start:
            if not regexp.startswith('^') or not regexp.endswith('$'):
                raise ValueError, 'Regexp %s must start with ^ and ends with $ - others are not supported; should be, if You post an usecase' % regexp
            if self.parsers_start.has_key(regexp):
                raise ValueError, 'Register already contains parser %s starting on %s; %s nod added' % (self.parsers_start[regexp], regexp, parser)

            registry(repr(self)).addClass(parser)
            self.parser_name_map[parser.name] = parser.__name__
            self.parsers_start[regexp] = parser

    def _addMacro(self, parser):
        if self.macro_map.has_key(parser.macro.name):
            raise ValueError, 'Macro %s already added under name %s' % (self.macro_map[parser.macro.name], parser.macro.name)
        self.macro_map[parser.macro.name] = parser.macro

    def addParsers(self, parsersList):
        for p in parsersList:
            self.add(p)

    def add(self, parser):
        self._addParser(parser)
        self._addMacro(parser)

    def get_parser(self, regexp):

        # should be better then has_key as mostly we will not raise exception
        try:
            return self.parsers_start[regexp]
        except KeyError:
            raise ValueError, 'No Parser in register starting with %s' % regexp

    def get_macro(self, name):
        try:
            return registry(repr(self)).getClass(self.parser_name_map[name]).macro
        except KeyError:
            raise ValueError, 'No macro parser registered under name %s in registry' % name

    def _most_matching(self, matching):
        most = None
        length = 0
        for m in matching:
            if len(m.string[m.start():m.end()]) > length:
                most = m
                length = len(m.string[m.start():m.end()])
        return (self.parsers_start[''.join([most.re.pattern, '$'])], m.string[m.start():m.end()])

    def resolve_parser(self, stream, map):
        matching = [compile(p[:-1]).match(stream) for p in self.parsers_start if compile(p[:-1]).match(stream)]
        if len(matching) == 0:
            return None
        parser, chunk = self._most_matching(matching)
        return parser(stream, self, chunk, map)

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
