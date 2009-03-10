# -*- coding: utf-8 -*-

""" Default document macro/nodes """

import logging

from macro import Macro
from parser import Parser, parse
from node import Node

__all__ = ['Document', 'DocumentParser', 'DocumentNode']

class Document(Macro):
    name = 'document'
    help = '<toto makro se nikdy nepouziva explicitne>'

    def parse_argument_string(self, argument_string):
        self.arguments = [argument_string]

    def expand_to_nodes(self, content, **kwargs):
        doc = DocumentNode()
        logging.debug('Creating document node and parsing document')
        res = parse(content, self.register_map, self.register)
        for node in res:
            if node is not None:
                doc.add_child(node)
        return doc


class DocumentParser(Parser):
    start = None
    macro = Document

    def resolve_argument_string(self):
        self.argument_string = self.stream
        self.stream = ''

#    def call_macro(self):
#        """ Do proper call to related macro(s) """
#        return self.macro(self.register, self.register_map).expand(self.content, self.parser)

class DocumentNode(Node): pass
