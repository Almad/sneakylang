# -*- coding: utf-8 -*-

""" Macro superclass and default Document and Macro classes """

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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

from err import *
import node
from macro_caller import ARGUMENT_SEPARATOR

class Macro(object):
    """ All macros should derive from this class """
    name = None # define macro name
    help = """<this macro haven't specified usage example>"""
    parsers_allowed = None

    def __init__(self, parser, register_map):
        self.parser = parser
        self.register_map = register_map

    @classmethod
    def parse_argument_string(self, argument_string):
        """ Return list of arguments. Uses ARGUMENT_SEPARATOR as argument separator.
        #TODO:
        By default, closing text in double quotes (") causes treating it as single argument, even if it contains
        argument separator. Nested quotes must not be escaped unless containting quote followed by argument
        separator; escape char is backslash (\)
        """
        return argument_string.split(ARGUMENT_SEPARATOR)

    @classmethod
    def argument_call(cls, argument_string, register=None, macro_instance=None):
        """ This function do proper call to expand with properly parsed argument_string.
        If you want to modify how argument string is parsed, overwrite parse_argument_string classmethod.
        If macro_instance is not given, macro is instantiazed with parser and register_map extracted
        from register argument.
        With or without instance, result of self.expand is returned."""
        if macro_instance is None:
            if register is None:
                raise ValueError, 'Either macro_instance or register must be given for performing argument_call'
            macro_instance = cls(register.parser_name_map[cls.name], register.register_map)
        if argument_string is None:
            return macro_instance.expand()
        else:
            return macro_instance.expand(*cls.parse_argument_string(argument_string))

    def expand(self, *args, **kwargs):
        """ Macro with arguments resolved; macro should expand themselves to Nodes and append to DOM """
        raise NotImplementedError

    def _get_register(self):
        """ Property function, use .register attribute instead """
        return self.register_map[self.parser.__class__]

    register = property(fget=_get_register)
