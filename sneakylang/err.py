# -*- coding: utf-8 -*-

""" SneakyLang-specific errors
"""

class Error(Exception): pass

class MacroCallError(Error):
    """ Error calling macro (i.e. bad arguments & co.) """

class ParserRollback(Error):
    """ Parser has taken activity, but decided that it's not its turn.
    Result should be that first char of chunk is treated as TextNode
    and main parser is proceeding """

class ExpanderError(Error):
    """ Error when expanding. Either internal problem with expander, or expander not found """
