#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for commons shared by tests """

import re

import logging
logging = logging.getLogger('sneakylang')

from sneakylang.err import ParserRollback, MacroCallError
from sneakylang.macro import Macro
from sneakylang.node import Node, TextNode
from sneakylang.parser import *
from sneakylang.expanders import Expander, expand

class DummyMacro(Macro):
    name = 'dummy_macro'

    def expand_to_nodes(self, *args, **kwargs):
        self.builder.append(DummyNode())

class DummyNode(Node):
    name = 'dummy node'

class DummyParser(Parser):
    start = ['(####)']
    macro = DummyMacro

class DummyParserTwo(Parser):
    start = ['(#####)']
    macro = DummyMacro

class NadpisMacro(Macro):
    name = 'nadpis'

    def expand_to_nodes(self, *args, **kwargs):
        return DummyNode()

# parser borrowed from czechtile
class Nadpis(Parser):
    start = ['(\n)?(=){1,5}(\ ){1}']
    macro = NadpisMacro

    def resolve_argument_string(self):
        endPattern = self.chunk[:-1]
        if endPattern.startswith('\n'):
            endPattern = endPattern[1:]
        # chunk is \n={n}[whitespace],
        # end is [whitespace]={n}\n
        endMatch = re.search(''.join([' ', endPattern, '\n']), self.stream)
        if not endMatch:
            raise ParserRollback
        self.level = len(endPattern)
        self.argument_string = self.stream[0:endMatch.start()]
        # end()-1 because we won't eat trailing newline
        self.chunk_end = self.stream[endMatch.start():endMatch.end()-1]
        self.stream = self.stream[endMatch.end()-1:]

    def call_macro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.register_map).expand(self.level, self.argument_string)

### Define basic grammar
# This wiki have only paragraps (\n\n) and headings (=)

class OneArgumentMacro(Macro):
    name = 'onearg'

    def expand_to_nodes(self, content):
        self.builder.append(DummyNode())
        self.builder.append(TextNode(content=content), move_actual=False)
        self.builder.move_up()

class ParagraphNode(Node): pass

class ParagraphMacro(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'
    parsersAllowed = ['Strong']

    @classmethod
    def get_arguments(self, argument_string):
        return [argument_string], {}

    def expand_to_nodes(self, *args):
        if len(args) < 1:
            raise MacroCallError("Paragraph must have some content")
        content = ''.join([word+' ' for word in args])[:-1]
        print content
        self.builder.append(ParagraphNode())
        parse(content, self.register_map, self.register, builder=self.builder)
        self.builder.move_up()

class Paragraph(Parser):
    start = ['(\n){2}']
    macro = ParagraphMacro
    end = '(\n){2}'

    def get_arguments(self, argument_string):
        return parse_macro_arguments(argument_string, return_kwargs=True)

    def resolve_argument_string(self):
        end = re.search(self.__class__.end, self.stream)
        if end:
            self.argument_string = self.stream[0:end.start()]
            self.chunk_end = self.stream[end.start():end.end()]
            self.stream = self.stream[end.end():]
        else:
            self.argument_string = self.stream
            print self.argument_string
            self.stream = ''

class StrongNode(Node): pass

class StrongMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand_to_nodes(self, content, **kwargs):
        self.builder.append(StrongNode(), move_actual=True)
        parse(content, self.register_map, self.register, builder=self.builder)
        self.builder.move_up()

class StrongVistingMacro(Macro):
    name = 'silne'
    help = '((silne zesileny text))'

    def expand_to_nodes(self, content, *args, **kwargs):
        self.state.visit(self)
        self.builder.append(StrongNode())
        self.builder.append(TextNode(content=content), move_actual=False)
        self.builder.move_up()

class PictureNode(Node):
    pass

class PictureKeywordMacro(Macro):
    name = 'picture'
    help = '((picture http://pic.png title="My picture"))'

    def expand_to_nodes(self, content, **kwargs):
        node = PictureNode()
        node.args = [content]
        node.kwargs = kwargs
        self.builder.append(node, move_actual=False)

class Strong(Parser):
    start = ['("){2}']
    macro = StrongMacro

    def resolve_argument_string(self):
        endMatch = re.search(re.escape(self.chunk), self.stream)
        if not endMatch:
            raise ParserRollback()
        self.argument_string = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

class ParagraphDocbookExpand(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<para>'] + [expand(child, format, node_map) for child in node.children] + ['</para>'])

parsers_list = [DummyParser, DummyParserTwo, Paragraph, Nadpis, Strong]
