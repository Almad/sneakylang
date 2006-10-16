#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Parsers
"""

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

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main,TestCase

logging.basicConfig(level=logging.DEBUG)

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import *
from sneakylang.register import Register

### Define basic grammar
# This wiki have only paragraps (\n\n) and headings (=)

class ParagraphNode(Node): pass

class ParagraphMacro(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand(self, content):
        p = ParagraphNode()
        nodes = parse(content, self.register)
        return p

class Paragraph(Parser):
    start = ['^(\n){2}$']
    macro = ParagraphMacro
    end = '^(\n){2}$'

    def resolveContent(self):
        self.stream = self.stream[len(self.chunk):]
        end = re.match(self.__class__.end, self.stream)
        if end:
            self.content = self.stream[0:end.end()]
            self.stream = self.stream[len(self.content):]
        else:
            self.content = self.stream
            self.stream = ''

    def callMacro(self):
        macro = self.__class__.macro(self.register)
        macro.expand(self.content)

### End of definition


class TestParsing(TestCase):
    def setUp(self):
        self.reg = Register()
        self.reg.add(Paragraph)

    def testPara(self):
        s = '''\n\nParagraph'''
        o = parse(s, self.reg)



if __name__ == "__main__":
    main()