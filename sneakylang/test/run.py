#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import imp
import os
import sys

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