#!/bin/bash
BIN=$1
FILE=$2
EXT="/Applications/Quantum.app/Contents/Resources/.kivy/extensions/plugins/"
MOD="/Applications/Quantum.app/Contents/Resources/.kivy/mods/"
PY="${BIN}/../PyCell/"
cp -r ${PY}Plugins/* ${MOD}
cp ${BIN}/${FILE} ${EXT}
install_name_tool -id ./Contents/Resources/.kivy/extensions/plugins/${FILE} ${EXT}${FILE}
echo "PyCell installed to $EXT"
#install_name_tool -change /Library/Frameworks/Python.framework/Versions/3.5/Python @executable_path/../Frameworks/python/3.5.0/Python ${DEST}${FILE}
#install_name_tool -change /usr/local/opt/boost-python/lib/libboost_python3.dylib @executable_path/lib/libboost_python3.dylib ${EXT}${FILE}
#install_name_tool -change /usr/local/opt/libiomp/lib/libiomp5.dylib @executable_path/lib/libiomp5.dylib ${EXT}${FILE}
#install_name_tool -change /usr/lib/libc++.1.dylib @executable_path/lib/libc++.1.dylib ${EXT}${FILE}
