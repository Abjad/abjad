#! /usr/bin/env python

from fileparser import FileParser
import os
import sys


if __name__ == '__main__':
   input_file = sys.argv[1]
   cur_dir = os.path.dirname(input_file)
   cur_dir = os.path.dirname(os.path.abspath(input_file))
   os.chdir(cur_dir)
   fileparser = FileParser(input_file, cur_dir)
   fileparser.parse( )
