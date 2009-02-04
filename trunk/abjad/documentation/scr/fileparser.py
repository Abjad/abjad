#! /usr/bin/env python

from abjad.cfg.cfg import ABJADPATH
from tags.abjadtag import ABJAD
from tags.class_names import CLASS_NAMES
from tags.comments import COMMENTS
from tags.definition import DEFINITION
from tags.interface import INTERFACE
from tags.lily import LILY
from tags.section import SECTION
from tags.subsection import SUBSECTION
from tags.to_do import TO_DO
from tags.toc_section import TOC_SECTION
import os


class FileParser(object):

   def __init__(self, filename, cur_dir):
      self.filename = filename.strip('.raw')
      self.input = open(filename, 'r').readlines( )
      self.output =  [ ]
      self.tags = [SECTION( ), SUBSECTION( ), INTERFACE( ), DEFINITION( ),
         COMMENTS( ), TO_DO( ), CLASS_NAMES( ), 
         TOC_SECTION( ),
         LILY( ), ABJAD(cur_dir)]

   @property
   def analytics(self):
      src1   = os.sep.join(['..'] * self.depth + ['templates', 'ga-1.js'])
      result =  '<script type="text/javascript" src="%s"></script>\n\n' % src1
      src2   = os.sep.join(['..'] * self.depth + ['templates', 'ga-2.js'])
      result += '<script type="text/javascript" src="%s"></script>\n\n' % src2
      return result

   @property
   def depth(self):
      if 'css' in os.listdir(os.curdir):
         return 0
      elif 'css' in os.listdir(os.pardir):
         return 1
      elif 'css' in os.listdir(os.pardir + os.sep + os.pardir):
         return 2
      elif 'css' in os.listdir(
         os.pardir + os.sep + os.pardir + os.sep + os.pardir):
         return 3
      else:
         raise ValueError('can not find doc root directory!')

   @property
   def docType(self):
      result =  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
      result += ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n' 
      result += '<html xmlns="http://www.w3.org/1999/xhtml" '
      result += 'lang="en" xml:lang="en">\n\n'
      return result

   @property
   def footer(self):
      footer = ['..'] * self.depth
      footer.append('index.html')
      footer = os.sep.join(footer)
      result = '\n<p class="footer"><a href="%s">Contents</a></p>'
      result %= footer
      result += '\n\n'
      result += '</div>'
      result += '\n\n'
      result += self.analytics
      result += '</body>\n\n</html>\n'
      return result

   @property
   def head(self):
      result  = '<head>\n\n'
      result += '<link rel="stylesheet" href="%s" type="text/css"/>'
      result %= self.stylesheet
      result += '\n\n'
      result += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>'
      result += '\n\n'
      result += '<title>The Abjad Doc Site</title>\n\n'
      result += '</head>\n\n'
      return result

   def parse(self):
      partial = self.input
      for tag in self.tags:
         #print "Processing %s tag..." % tag.__class__.__name__
         tag.parse(partial)
         partial = tag.output
      self.output = partial
      self.writeOutput( )

   @property
   def stylesheet(self):
      stylesheet = ['..'] * self.depth
      stylesheet.append('css%sabjad.css' % os.sep)
      stylesheet = os.sep.join(stylesheet)
      return stylesheet

   def writeOutput(self):
      if self.output:
         out = open(self.filename + '.html', 'w')
         self.output.insert(0, '<body>\n\n<div id="content">\n\n')
         self.output.insert(0, self.head)
         self.output.insert(0, self.docType)
         self.output.append(self.footer)
         out.writelines(self.output)
         out.close( )
      else:
         print "Did not write output file because output is empty."
