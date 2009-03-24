#!/usr/bin/env python

import os
import sys

import nose

WORKING_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

if __name__ == "__main__":
    if not WORKING_DIR in sys.path:
        sys.path.insert(0, WORKING_DIR)
    nose.run_exit()
