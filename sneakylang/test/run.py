#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
# SneakyLang: Extensible WikiFramework
#Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
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

import unittest
import imp
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def getSuites():
    tests = []
    for i in os.listdir(os.curdir):
        if i.startswith("test_") and i.endswith(".py"):
            tests.append(imp.load_source(i[5:-3], i))
    return tests

def runTests(tests):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test in tests:
        testSuite = loader.loadTestsFromModule(test)
        suite.addTests(testSuite)
    unittest.TextTestRunner(verbosity=1, descriptions=1).run(suite)

def main():
    try:
        import nose
        cover = False
        if len(sys.argv) > 1 and sys.argv[1] == "-c":
            import coverage
            coverage.start()
            cover = True
            del sys.argv[1]
        nose.run()
        if cover:
            coverage.stop()
            moduleList = [mod for name, mod in sys.modules.copy().iteritems()
            if getattr(mod, '__file__', None) and
            name.startswith('sneakylang.') and
            'test' not in name
            ]
            moduleList.sort()
            coverage.report(moduleList)

    except ImportError:
        # dirty unittest run
        tests = getSuites()
        runTests(tests)

if __name__ == "__main__":
    main()