#! /usr/bin/env python

import os
import re
import sys


class FileParser(object):
   def __init__(self, filename):
      self.filename = filename.strip('.raw')
      #self.output =  open(filename.strip('.raw') + '.html', 'w')
      self.input = open(filename, 'r').readlines( )
      self.output =  [ ]
      self.tags = [PRE( ), LILY( )]

   def writeOutput(self):
      if self.output:
         out = open(self.filename + '.html', 'w')
         out.writelines(self.output)
         out.close( )
      else:
         print "Did not write output file because output is empty."
         
   def parse(self):
      partial = self.input
      for tag in self.tags:
         print "\nProcessing %s tag..." % tag.__class__.__name__
         tag.parse(partial)
         partial = tag.output
      self.output = partial
      self.writeOutput( )
      

class _TagParser(object):

   def __init__(self):
      self.output = [ ]

   def parse(self):
      pass

class LILY(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<lily>' in line:
            self.output.append('<pre class="lilypond">\n')
         elif '</lily>' in line:
            self.output.append('</pre>\n')
         else:
            #self.output.append(line.strip(' '))
            self.output.append(line)


class PRE(_TagParser):

   def write_inline_img(self, out, prev_image_number):
      out.append('</pre>\n')
      out.append('<image class="inline" src="images/%s.png">\n' % 
         prev_image_number)
      out.append('<pre>\n')

   def write_terminal_img(self, out, prev_image_number):
      out.append('<image src="images/%s.png">\n' % prev_image_number)

   def parse(self, lines):
      pattern = re.compile('abjad> ')
      hide_me_pattern = re.compile('hide> ')
      inline_indicator = '<!-- inline -->'

      found_abjad_directive = False
      found_show = False
      found_inline = False
      image_number = 1

      for line in lines:
         just_closed_tag = False
         if '<pre>' in line:
            found_abjad_directive = True
            tmp_aj = open('tmp.aj', 'w')
            tmp_aj.write('from abjad import *\n')
         elif '</pre>' in line:
            found_abjad_directive = False
            #found_show = False
            if not tmp_aj.closed:
               tmp_aj.close( )
            just_closed_tag = True
            #image_number += 1
         elif inline_indicator in line:
            found_inline = True
         elif found_abjad_directive and ('abjad> ' in line or 'hide> ' in line):
            if found_show:
               self.write_inline_img(self.output, image_number - 1)
               tmp_aj = open('tmp.aj', 'w')
               tmp_aj.write('from abjad import *\n')
               found_show = False
            if 'abjad> ' in line:
               abjad_directive = pattern.split(line)[-1]
            elif 'hide> ' in line:
               abjad_directive = hide_me_pattern.split(line)[-1]
            # keep adding successive lines of directives to the tempfile
            if not abjad_directive.startswith('show'):
               tmp_aj.write(abjad_directive)
            # compile the example after the last line makes it into the tempfile
            else:
               found_show = True
               # strip 'show(' from beginning of line
               lily_object = abjad_directive[5:]
               lily_object = lily_object.strip(')\n')
               tmp_aj.write("tmp_ly = open('%s.ly', 'w')\n" % image_number)
               tmp_aj.write("""tmp_ly.write('\\\\version "2.11.56"\\n')\n""")
               tmp_aj.write("""tmp_ly.write('\\\\include "english.ly"\\n')\n""")
               tmp_aj.write(
                  """tmp_ly.write('\\\\include "%s/scm/abjad.scm"\\n')\n""" %
                  ABJADPATH)
               tmp_aj.write(
                  """tmp_ly.write('\\\\include "%s/layout/web.ly"\\n')\n""" %
                  ABJADPATH)
               tmp_aj.write(
                  """tmp_ly.write('\\\\layout { ragged-right = ##t }\\n')\n""")
               tmp_aj.write("""tmp_ly.write('\\n')\n""")
               tmp_aj.write(
                  """tmp_ly.write('\\\\header{ tagline = "" }\\n')\n""")
               tmp_aj.write(
                  """tmp_ly.write("{ %%s\\n }" %% %s.format)\n""" % lily_object) 
               tmp_aj.write("""tmp_ly.close( )""")
               tmp_aj.close( )
               os.popen('python tmp.aj')
               os.popen('lilypond --png -dresolution=300 %s.ly' % image_number)
               os.popen('rm %s.ps' % image_number)
               os.popen('rm %s.ly' % image_number)
               os.popen('mv %s.png images' % image_number)
               os.popen(
                  'convert images/%s.png -trim -resample 40%% images/%s.png' % 
                  (image_number, image_number))
               image_number += 1

         # faithfully copy over line from input to outputfile;
         # embed image if deemed necessary earlier in loop above
         if inline_indicator not in line: 
            if 'hide> ' not in line:
               #self.output.append(line.strip(' '))
               self.output.append(line)
         if just_closed_tag:
            prev_image_number = image_number - 1
            if found_show:
               if found_inline:
                  self.output.append(
                     '<image class="inline" src="images/%s.png">\n' % 
                     prev_image_number)
               else:
                  self.output.append(
                     '<image src="images/%s.png">\n' % prev_image_number)
            found_show = False
            found_inline = False

      try:
         os.stat('tmp.aj')
         os.popen('rm tmp.aj')
      except:
         pass


#### EXECUTABLE ####

ABJADPATH = os.environ['ABJADPATH']

if __name__ == '__main__':
   try:
      fileparser = FileParser(sys.argv[1])
      #out = open(sys.argv[1].strip('.raw') + '.html', 'w')
   except:
      raise Exception('requires one commandline argument.')

   fileparser.parse( )
   #print fileparser.output
