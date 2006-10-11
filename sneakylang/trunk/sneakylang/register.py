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

from classregistry import registry

class Register:
    def __init__(self):
        self.parsers_start = {}
        self.parser_name_map = {}
        self.macro_map = {}

    def _addParser(self, parser):
        for regexp in parser.parser_start:
            if not regexp.startswith('^') or not regexp.endswith('$'):
                raise ValueError, 'Regexp %s must start with ^ and ends with $ - others are not supported; should be, if You post an usecase' % regexp
            if self.parsers_start.has_key(regexp):
                raise ValueError, 'Register already contains parser %s starting on %s; %s nod added' % (nodes_start[regexp], regexp, parser)

            registry(str(self)).addClass(parser)
            self.parser_name_map[parser.name] = parser.__name__
            self.parsers_start[regexp] = parser

    def _addMacro(self, parser):
        if self.macro_map.has_key(parser.macro.name):
            raise ValueError, 'Macro %s already added under name %s' % (self.macro_map[parser.macro.name], parser.macro.name)
        self.macro_map[parser.macro.name] = parser.macro

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
            return registry(str(self)).getClass(self.parser_name_map[name]).macro
        except KeyError:
            raise ValueError, 'No macro parser registered under name %s in registry' % name