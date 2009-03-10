# -*- coding: utf-8 -*-

""" Hooks around macos.
Hooks works on same base as SAX events. When macro is encountered in document,
callback is called on all registered hooks.

Pre- macro hooks are useful for modifying macro arguments or parsed stream.
Post- macro hooks are useful for rebuilding or inspecting tree
"""

class MacroHook(object):
    """ Main MacroHook class. Subclass this one to make real MacroHook """
    macro = None

    def pre_macro(self, stream, macro, tree):
        return stream

    def post_macro(self, macro, builder):
        pass
