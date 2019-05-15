#!/bin/bash

LINE=`egrep -i '[^ \t]*set[ \t]*\([ \t]*'"$1"'(.*)\)' ../CMakeLists.txt`
echo $LINE | sed -ne 's/^\s*set\s*(\s*\(.*\)\s*)\s*$/\1/pi' | awk -F'"' '{ print $2 }'
