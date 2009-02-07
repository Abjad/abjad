#! /usr/bin/env python

from abjad.cfg.cfg import ABJADPATH
from mako.template import Template
from mako.lookup import TemplateLookup
import codecs
import getopt
import os
import sys

#templates_dir = os.environ['ABJADPATH'] + '/documentation/templates'
templates_dir = ABJADPATH + os.sep.join(['documentation', 'templates'])


### TODO: make this system-independent using os.path

def get_file_directory(filename):
   try:
      indx = filename.rindex('/')
   except ValueError:
      return ''
   return filename[0:indx+1]

def process_file(filename):
   #content = open(filename, 'r')
   content = codecs.open(filename, 'r', encoding = 'utf-8')
   content_string = content.read( )
   content.close( )
   tlookup = TemplateLookup(directories=['templates_dir'])
   t = Template(filename=templates_dir + '/template.html', lookup = tlookup)
   #result =  t.render(content=content_string)
   result =  t.render_unicode(content=content_string)

   out_dir = get_file_directory(filename) 
   #out = open(out_dir + 'index.html', 'w')
   out = codecs.open(out_dir + 'index.html', 'w', encoding = 'utf-8')
   out.write(result)
   out.close( )

def usage( ):
   print "Pass filename with -f flag."

def main(argv):
   try:
      opts, args = getopt.getopt(argv, 'f:', ["filename"])
   except getopt.GetoptError, err:
      print str(err)
      sys.exit(2)
   if args:
      usage( )
      sys.exit(2)
   for o, a in opts:
      if o in ('-f', '--filename'):
         if not a.endswith('.html'):
            print "Sorry, will only process html files."
         else:
            process_file(a)
      else:
         assert False, 'unhandled option'


if __name__ == '__main__':
   main(sys.argv[1:])
