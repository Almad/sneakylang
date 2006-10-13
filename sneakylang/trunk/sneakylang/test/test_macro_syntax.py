#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test Possibility of directly calling macro
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
#Parsers
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging

from unittest import main,TestCase

logging.basicConfig(level=logging.DEBUG)

from sneakylang.macro import Macro
from sneakylang.node import Node
from sneakylang.parser import Parser
from sneakylang.register import Register

### Define basic grammar

class Paragraph(Parser):
    start = ['^(\n){2}$']
    macro = MacroParagraph

    def callMacro(self, stream):
        content = stream[0:re.match('(\n){2}').end()]
        stream = stream[0, len(content)-2]
        macro = Paragraph()
        macro.expand(self.dom, content)


### End of definition


class TestParsing(TestCase):
    pass


if __name__ == "__main__":
    main()