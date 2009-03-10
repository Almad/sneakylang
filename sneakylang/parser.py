# -*- coding: utf-8 -*-

"""
Parser transforming input stream to DOM
"""

import logging

from err import ParserRollback, MacroCallError

from node import TextNode
from register import Register
from treebuilder import TreeBuilder

#FIXME
NEGATION_CHAR = "!"

__all__ = ['Parser', 'parse']

class Parser(object):
    """ All parsers should derivate from this class """
    start = []
    macro = None

    def __init__(self, stream, parent_parser, chunk, register):
        """ Parse is taking activity in DOM dom because of chunk resolved """
        self.chunk = chunk
        self.parent_parser = parent_parser
        self.argument_string = ''
        self.init()
        self.stream = stream[len(chunk):]
        self._register = register

    def init(self):
        """ Something to do after init? ,) """
        pass

    def begin_parse(self):
        """ Begin parsing, set up needed things, determine whether to append
        stream to chunk or mark chunk as node_start
        """
        pass

    def _get_macro(self, builder, state):
        return self.macro.argument_call(self.argument_string, self.register, builder, state)

    def resolve_argument_string(self):
        """ Resolve transform content to argument string which would be used if calling macro by macro syntax """

    def get_macro(self, builder, state):
        """ Return properly istantiazed macro and new stream """
        self.begin_parse()
        self.resolve_argument_string()
        return (self._get_macro(builder, state), self.stream)

    def parse(self):
        macro, self.stream = self.get_macro()
        return macro.expand()
#        self.dom_tree = self.call_macro()
#        return self.dom_tree

    def get_register(self):
        if self._register is not None:
            return self._register
        else:
            return self.register_map[self.__class__]

    register = property(fget=get_register)

def _get_text_node(stream, register, register_map, builder, state, force_first_char=False, opened_text_node=None, whole_stream=None):
    if opened_text_node is None:
        tn = TextNode()
    else:
        tn = opened_text_node

    if force_first_char is True:
        tn.content = u''.join([tn.content, stream[0:1]])
        stream = stream[1:]

    if whole_stream is None:
        whole_stream = stream

    while True:
        try:
            res = register.resolve_macro(stream, builder, state, whole_stream)
        except (ParserRollback, MacroCallError):
            pass
        else:
            if res != (None, None):
                break
        if len(stream) == 0:
            break
        tn.content = u''.join([tn.content, stream[0:1]])
        stream = stream[1:]
    return (tn, stream)

def parse(stream, register_map, register=None, parsers=None, state=None, builder=None, document_root=False):
    if builder is None:
        builder = TreeBuilder()

    if isinstance(stream, str):
        stream = stream.decode('utf-8')

    if builder.root is None:
        if document_root is True:
            from document import DocumentNode
            builder.set_root(DocumentNode())
            hack_root = False
        else:
            from node import Node
            builder.set_root(Node())
            hack_root = True
    else:
        hack_root = False

    remembered_actual_node = builder.actual_node

    if register is None:
        register = Register([p for p in register_map])
        register.visit_register_map(register_map)
        if parsers is not None:
            register.add_parsers(parsers)

    opened_text_node = None

    whole_stream = stream
    while len(stream) > 0:
        assert isinstance(stream, unicode) == True, stream
        try:
            macro, stream_new = register.resolve_macro(stream, builder, state, whole_stream)
            if macro is not None and stream_new is not None:
                # negation in effect?
                if opened_text_node is not None and opened_text_node.content.endswith(NEGATION_CHAR):
                    # don't forget to eat negation char!
                    opened_text_node.content = opened_text_node.content[:-1]
                    raise ParserRollback("Negation resolved")

                logging.debug('Resolved macro %s' % macro)
                stream_new = register_map.pre_hooks(stream_new, macro, builder)
                macro.expand(builder=builder, state=state)
                register_map.post_hooks(macro, builder)
                stream = stream_new
                opened_text_node = None
            else:
                # macro not resolved, add text node
                node, stream = _get_text_node(stream, register, register_map, builder, state, opened_text_node=opened_text_node, whole_stream=whole_stream)
                if opened_text_node is None:
                    builder.append(node, move_actual=False)
                opened_text_node=node
        except (ParserRollback, MacroCallError):
            #badly resolved macro
            logging.debug('Catched ParseRollback, forcing text char')
            node, stream = _get_text_node(stream, register, register_map, builder, state, True, opened_text_node=opened_text_node, whole_stream=whole_stream)
            if opened_text_node is None:
                builder.append(node, move_actual=False)
            opened_text_node=node

    if hack_root is True:
        builder.move_up()

    # make sure that we have ended where we have begun
    assert builder.actual_node == remembered_actual_node, "remembered %s, but actual node is %s" % (remembered_actual_node, builder.actual_node)

    if hack_root is False:
        return builder.root
    else:
        return builder.root.children
