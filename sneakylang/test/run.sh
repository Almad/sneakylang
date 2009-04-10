#!/bin/sh

cd `dirname $0`
cmd="nosetests `pwd`/test_*.py $@"
echo "*** Running: $cmd"
echo
$cmd
