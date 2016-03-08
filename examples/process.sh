#!/usr/bin/env bash
#
# Runs syntax highlighter on code examples
#
# Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>
#
pygmentize -l llvm -f latex -O style=solarizedlight -o annotations.tex annotations.txt
