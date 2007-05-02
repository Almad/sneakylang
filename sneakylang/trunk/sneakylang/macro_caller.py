# -*- coding: utf-8 -*-

""" Set of funcitons and constants
needed to perform proper call when calling macros with
extensive syntax ((macro_name argument argument))

All those functions are meant to be overwritten by
implementation and should be as forward-compatible as possible.
 """

###
# SneakyLang: Extensible WikiFramework
# Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
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
from types import StringType

from err import *

ARGUMENT_SEPARATOR = ' '

# separator between macro name and it's argus
# should be f.e. ( if macro syntax whould be #macro_name(arg,arg,arg)
MACRO_NAME_ARGUMENT_SEPARATOR = ' '

# macro_begin should be either string (faster),
# or compiled re pattern object (allows more complex macro syntax)
# pattern object should begin with ^ as search is performed and macro
# on beginning of the string assumed
MACRO_BEGIN = '(('

MACRO_END = '))'

# Whether macro must be oneliner ((macro arg arg)), or should be defined multiline
# ((macro
#        arg
#        arg2
# ))
ALLOW_MULTILINE_MACRO = False

def resolve_macro_name(stream):
    """ Resolve macro name. Return tuple(macro_name, string_with_macro_arguments) """
    if isinstance(MACRO_NAME_ARGUMENT_SEPARATOR, StringType):
        # if name_argument separator not in stream, then no argument given - return whole string
        # Please report other use-cases as bug
        res = stream.split(MACRO_NAME_ARGUMENT_SEPARATOR)
        if len(res) == 1:
            return (res[0], None)
        if len(res) == 2:
            return (res[0], res[1])
        else:
            return (res[0], ''.join([''.join([arg, ARGUMENT_SEPARATOR]) for arg in res[1:]])[:-len(ARGUMENT_SEPARATOR)])
    else:
        raise NotImplementedError, 'MACRO_NAME_ARGUMENT_SEPARATOR must be string, other types like regexp are not yet supported'

def resolve_name_from_register(stream, register):
    name = resolve_macro_name(stream)[0]
    # if name is None, it's not resolved in name_map, so explicit check not needed
    if name in register.macro_map:
        return name
    else:
        return None

def get_content(stream):
    """ Return content of macro or None if proper end not resolved """
    if not ALLOW_MULTILINE_MACRO:
        #FIXME: (?) allow regexp macro_end...?
        this_line = stream.split('\n')[0]
        if MACRO_END not in this_line:
            return None
        # FIXME: Remember for )) in "enclosed argument", which should be
        # not considered as macro end
        return this_line.split(MACRO_END)[0]


    else:
        raise NotImplementedError, 'Multiline macros not implemented yet'

def process_resolved_macro(stream, register):
    macro_content = get_content(stream)
    if macro_content is None:
        return None
    else:
        return resolve_name_from_register(macro_content, register)

def get_macro_name(stream, register):
    """ Resolve if stream is beginning with macro.
    If yes, name is resolved and returned, otherwise function returns None
    """

    # first resolve if macro syntax
    if isinstance(MACRO_BEGIN, StringType):
        if not stream.startswith(MACRO_BEGIN):
            return None
        else:
            return process_resolved_macro(stream[len(MACRO_BEGIN):], register)

    else:
        # compiled regular expression assumed
        res = MACRO_BEGIN.search(stream)
        if res is None:
            return None
        else:
            return process_resolved_macro(stream[res.end():], register)

    raise NotImplementedError, 'String not parsed in macro in one of possible MACRO_BEGIN instances, please report this as bug.'

def call_macro(macro, argument_string, register, builder, state):
    macro.argument_call(argument_string, register, builder, state).expand()

def expand_macro_from_stream(stream, register, builder, state):
    """ Stream is beginning with properly written macro, create proper macro and return
    return tuple(macro_instance, stripped_stream)
    """
    #FIXME: OMG, get this regexp syntax working
    if not isinstance(MACRO_BEGIN, StringType):
        raise NotImplementedError, 'MACRO_BEGIN must be string, regular expressions not yet supported'

    macro_content = get_content(stream[len(MACRO_BEGIN):])
    # assuming macro previously resolved in context
    name, args = resolve_macro_name(macro_content)
    new_stream = stream[len(MACRO_BEGIN)+len(macro_content)+len(MACRO_END):]
    return (register.macro_map[name].argument_call(args, register, builder, state), new_stream)