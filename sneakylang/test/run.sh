#!/bin/sh
for i in `ls test*py`; do nosetests $i; done;
