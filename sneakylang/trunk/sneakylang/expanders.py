# -*- coding: utf-8 -*-

""" Expanders for nodes
"""

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
# and contributors, for complete list see
# http://projects.almad.net/czechtile/wiki/Contributors
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

class Expander:
    def expand(self, text):
        raise NotImplementedError, 'Expander do not support expand...WTF is that?'

class Xhtml11Expander(Expander): pass
class Docbook5Expander(Expander): pass

""" Expanders have to be singletons having one expand method.
"""

class _ParagraphXhtmlExpander(Xhtml11Expander):
    def expand(self, text):
        return ''.join(['<p>', text, '</p>'])
paragraphXhtmlExpander = _ParagraphXhtmlExpander()


class _ParagraphDocbook5Expander(Docbook5Expander):
    def expand(self, text):
        return ''.join(['<para>', text, '</para>'])
paragraphDocbook5Expander = _ParagraphDocbook5Expander()

