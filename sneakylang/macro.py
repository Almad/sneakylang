# -*- coding: utf-8 -*-
""" Macro superclass and default Document and Macro classes """

import logging
logging = logging.getLogger('sneakylang')

from err import *
from macro_caller import parse_macro_arguments

class Macro(object):
    """ All macros should derive from this class """
    name = None # define macro name
    help = """<this macro haven't specified usage example>"""
    parsers_allowed = None

    def __init__(self, register_map, builder, state=None):
        object.__init__(self)
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
        else:
            self.arguments = []
            self.keyword_arguments = {}

    @classmethod
    def argument_call(cls, argument_string, register, builder, state):
        """ argument_string - string as it would be called by macro syntax
        returns properly istantiazed macro, ready call expand() function """
        assert type(argument_string) in (type(None), type(''), type(u'')), u"Bad argument_string type %s (content: %s)" % (type(argument_string), argument_string)
        macro_instance = cls(register.register_map, builder, state)
        macro_instance.parse_argument_string(argument_string)
        return macro_instance

    def expand(self, **kwargs):
        try:
            return self.expand_to_nodes(*self.arguments, **self.keyword_arguments)
        except TypeError, err:
            logging.debug("Error while calling macro %s: %s" % (self.__class__, err))
            raise MacroCallError(err)

    def expand_to_nodes(self, *args, **kwargs):
        """ Macro with arguments resolved; macro should expand themselves to Nodes and append to DOM """
        raise NotImplementedError()

    def _get_register(self):
        """ Property function, use .register attribute instead """
        if self.register_map.has_key(self.__class__):
            return self.register_map[self.__class__]
        else:
            from register import Register
            return Register()

    register = property(fget=_get_register)
