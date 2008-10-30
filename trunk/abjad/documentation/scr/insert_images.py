#! /usr/bin/env python

import os
import re
import sys

ABJADPATH = os.environ['ABJADPATH']

try:
   f = open(sys.argv[1], 'r')
   out = open(sys.argv[1].strip('.raw') + '.html', 'w')
except:
   raise Exception('requires one commandline argument.')

def write_inline_img(out, prev_image_number):
   out.write('</pre>\n')
   out.write('<image class="inline" src="images/%s.png">\n' % prev_image_number)
   out.write('<pre>\n')

def write_terminal_img(out, prev_image_number):
   out.write('<image src="images/%s.png">\n' % prev_image_number)

pattern = re.compile('abjad> ')
hide_me_pattern = re.compile('hide> ')
inline_indicator = '<!-- inline -->'

found_abjad_directive = False
found_show = False
found_inline = False
image_number = 1

for line in f.readlines( ):
   just_closed_tag = False
   #if '<pre>' in line:
   if '<pre' in line:
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
         write_inline_img(out, image_number - 1)
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
         tmp_aj.write("""tmp_ly.write('\\\\header{ tagline = "" }\\n')\n""")
         tmp_aj.write(
            """tmp_ly.write("{ %%s\\n }" %% %s.format)\n""" % lily_object) 
         tmp_aj.write("""tmp_ly.close( )""")
         tmp_aj.close( )
         os.popen('python tmp.aj')
         os.popen('lilypond --png -dresolution=300 %s.ly' % image_number)
         os.popen('rm %s.ps' % image_number)
         os.popen('rm %s.ly' % image_number)
         os.popen('mv %s.png images' % image_number)
         os.popen('convert images/%s.png -trim -resample 40%% images/%s.png' % 
            (image_number, image_number))
         image_number += 1

   # faithfully copy over line from input to outputfile;
   # embed image if deemed necessary earlier in loop above
   if inline_indicator not in line: 
      if 'hide> ' not in line:
         #out.write(line)
         out.write(line.strip(' '))
   if just_closed_tag:
      prev_image_number = image_number - 1
      if found_show:
         if found_inline:
            out.write('<image class="inline" src="images/%s.png">\n' % 
               prev_image_number)
         else:
            out.write('<image src="images/%s.png">\n' % prev_image_number)
      found_show = False
      found_inline = False

try:
   os.stat('tmp.aj')
   os.popen('rm tmp.aj')
except:
   pass
