# -*- coding: utf-8 -*-

""" SneakyLang: Extensible WikiFramework """

VERSION = (0, 3, 1)

__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


from document import Document
from expanders import expand
from macro import Macro
from parser import parse
from register import Register, RegisterMap
from treebuilder import TreeBuilder

__all__ = (
    "Document", "Macro", "Register", "RegisterMap", "TreeBuilder",
    "parse", "expand",
)
