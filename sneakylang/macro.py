# -*- coding: utf-8 -*-

""" Macro superclass and default Document and Macro classes """

###
# SneakyLang: Extensible WikiFramework
# Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/sneakylang/wiki/Contributors
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

import re
import logging
logging = logging.getLogger('sneakylang')

from err import *
import node
from macro_caller import parse_macro_arguments

class Macro(object):
    """ All macros should derive from this class """
    name = None # define macro name
    help = """<this macro haven't specified usage example>"""
    parsers_allowed = None

    def __init__(self, register_map, builder, state=None):
        self.register_map = register_map
        self.arguments = []
        self.keyword_arguments = {}
        self.builder = builder
        self.state = state

    def get_argument_list(self, argument_string):
        """ DEPRECATED: Use get_arguments instead. 
        Return list of arguments. Uses ARGUMENT_SEPARATOR as argument separator."""
        return parse_macro_arguments(argument_string)

    def get_arguments(self, argument_string):
        return parse_macro_arguments(argument_string, return_kwargs=True)

    def parse_argument_string(self, argument_string):
        if argument_string is not None and argument_string not in (u'', ''):
            self.arguments, self.keyword_arguments = self.get_arguments(argument_string)

    @classmethod
    def argument_call(cls, argument_string, register, builder, state):
        """ argument_string - string as it would be called by macro syntax
        returns properly istantiazed macro, ready call expand() function """
        assert type(argument_string) in (type(None), type(''), type(u'')), str(argument_string)
        macro_instance = cls(register.register_map, builder, state)
        macro_instance.parse_argument_string(argument_string)
        return macro_instance

    def expand(self, **kwargs):
        try:
            return self.expand_to_nodes(*self.arguments)
        except TypeError, err:
            raise MacroCallError, err

    def expand_to_nodes(self, *args, **kwargs):
        """ Macro with arguments resolved; macro should expand themselves to Nodes and append to DOM """
        raise NotImplementedError

    def _get_register(self):
        """ Property function, use .register attribute instead """
        if self.register_map.has_key(self.__class__):
            return self.register_map[self.__class__]
        else:
            from register import Register
            return Register()

    register = property(fget=_get_register)
