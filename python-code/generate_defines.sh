#!/bin/bash

PYTHON_VERSION="3.8"

PATH_TO_KSP_DISPLAY="../../ksp_main_controller/src"
PYTHON_INSTALL="/usr/include/python$PYTHON_VERSION"
#PYTHON_INSTALL="/cygdrive/c/Users/mkluge/Anaconda3/include"

cp $PATH_TO_KSP_DISPLAY/ksp_display_defines.h .
swig -python -module ksp_console ksp_display_defines.h
gcc -c -fpic ksp_display_defines_wrap.c -o ksp_display_defines_wrap.o -I$PYTHON_INSTALL -I.
gcc -shared ksp_display_defines_wrap.o -o _ksp_console.so -lpython$PYTHON_VERSION
