#!/bin/bash
set -x
set -e
BIN=$1
FILE=$2
EXT="/Applications/Quantum.app/Contents/Resources/.kivy/extensions/plugins/"
MOD="/Applications/Quantum.app/Contents/Resources/.kivy/mods/"
PY="${BIN}/../PyCell/"
osxrelocator -r . ./Contents @executable_path/..
osxrelocator -r . ./build @executable_path/../Resources/.kivy/extensions/plugins
if [ ! -d ${EXT} ]; then
  mkdir ${EXT}
fi;
if [ ! -d ${MOD}/UDPyCell ]; then
  mkdir ${MOD}/UDPyCell;
fi;
cp -r ${PY}Plugins/* ${MOD}
cp ${BIN}/${FILE} ${EXT}
{
echo "cp -r ${PY}Plugins/* ${MOD}"
echo "if [ ! -d ${MOD}/UDPyCell ]; then mkdir ${MOD}/UDPyCell; fi;"
} > refresh.sh;
chmod 744 refresh.sh;
echo "PyCell installed to $EXT";
