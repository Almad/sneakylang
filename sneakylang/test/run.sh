#!/bin/sh

cmd="nosetests `pwd`/test_*.py $@"
echo "*** Running: $cmd"
echo
$cmd
