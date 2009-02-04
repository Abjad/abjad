from abjad.cfg.cfg import ABJADPATH
from tagparser import _TagParser
import os
import re


### TODO - All calls here to os.popen( ) are deprecated in Python 2.6.
###        Use the Ptyhon 'subprocess' module instead.
###        See http://docs.python.org/library/subprocess.html#module-subprocess
###        See PEP 324 at http://www.python.org/dev/peps/pep-0324/

class ABJAD(_TagParser):

   def __init__(self, curdir):
      self.curdir = curdir
      self.output = [ ]
      self.cur_image_number = 1
      self.within_abjad_block = False
      self.last_open_abjad_idx = -1
      self.found_image_request = False
      self.found_code_request = False
      self.pattern = re.compile('abjad> ')
      self.hide_me_pattern = re.compile('hide> ')

   def parse(self, lines):
      for line in lines:
         if '<abjad>' in line:
            self.handle_open_tag(line)
         elif '</abjad>' in line:
            self.handle_close_tag(line)
         elif self.within_abjad_block:
            self.handle_internal_line(line)
         else:
            self.output.append(line)
      self.clean_up( )
   
   def handle_open_tag(self, line):
      if self.within_abjad_block:
         print 'ERROR: nested <abjad> tags.'
      else:
         self.within_abjad_block = True
         self.output.append('<pre class="abjad">\n')
         self.last_open_abjad_idx = len(self.output) - 1
         ### TODO - replace with portable os.tmpfile( )
         self.tmp_aj = open('tmp.aj', 'w')
         self.tmp_aj.write('from abjad import *\n')

   def handle_close_tag(self, line):
      if not self.within_abjad_block:
         print 'ERROR: unmatched </abjad> tag.'
      else:
         self.within_abjad_block = False
         if self.found_code_request:
            self.output.append('</pre>\n')
         if self.found_image_request:
            image = '<img alt="" src="images/%s.png"/>\n'
            self.output.append(image % self.cur_image_number)
            self.cur_image_number += 1
         if not self.found_code_request:
            self.output.pop(self.last_open_abjad_idx)
         self.found_code_request = False
         self.found_image_request = False

   def handle_internal_line(self, line):
      if 'abjad>' in line:
         self.found_code_request = True
         self.output.append(line.strip(' '))
         abjad_directive = self.pattern.split(line)[-1]
      elif 'hide> ' in line:
         abjad_directive = self.hide_me_pattern.split(line)[-1]
      else:
         abjad_directive = None
      if not abjad_directive:
         self.output.append(line.strip(' '))
      elif not abjad_directive.startswith('show'):
         self.tmp_aj.write(abjad_directive)
      else:
         self.found_image_request = True
         # strip 'show(' from beginning of line
         lily_object = abjad_directive[5:]
         lily_object = lily_object.strip(')\n')
         self.write_lily_object(self.tmp_aj, lily_object)
         self.make_image( )

   def write_lily_object(self, tmp_aj, lily_object):
      #tmp_aj.write("tmp_ly = open('%s.ly', 'w')\n" % self.cur_image_number)
      #tmp_aj.write("tmp_ly = open('%s%s%s.ly', 'w')\n" % (
      #   CURDIR, os.sep, self.cur_image_number))
      tmp_aj.write("tmp_ly = open('%s%s%s.ly', 'w')\n" % (
         self.curdir, os.sep, self.cur_image_number))
      #from abjad.cfg.lilypond_version import lilypond_version
      from abjad.cfg.lilypond_version import _get_lilypond_version
      tmp_aj.write("""tmp_ly.write('\\\\version "%s"\\n')\n""" % 
         _get_lilypond_version( ))
      tmp_aj.write("""tmp_ly.write('\\\\include "english.ly"\\n')\n""")
      scm = os.sep.join([ABJADPATH, 'scm', 'abjad.scm'])
      tmp_aj.write("""tmp_ly.write('\\\\include "%s"\\n')\n""" % scm)
      layout = os.sep.join([ABJADPATH, 'layout', 'web.ly'])
      tmp_aj.write("""tmp_ly.write('\\\\include "%s"\\n')\n""" % layout)
      tmp_aj.write(
         """tmp_ly.write('\\\\layout { ragged-right = ##t }\\n')\n""")
      tmp_aj.write("""tmp_ly.write('\\n')\n""")
      tmp_aj.write("""tmp_ly.write('\\\\header{ tagline = "" }\\n')\n""")
      tmp_aj.write(
         """tmp_ly.write("{ %%s\\n }" %% %s.format)\n""" % lily_object) 
      tmp_aj.write("""tmp_ly.close( )""")
      tmp_aj.close( )

   def make_image(self):
      num = self.cur_image_number
      os.popen('python tmp.aj')
      os.popen('lilypond --png -dresolution=300 %s.ly' % num)
      os.popen('rm %s.ps' % num)
      os.popen('rm %s.ly' % num)
      os.popen('mv %s.png images' % num)
      output = 'convert images/%s.png -trim -resample 40%% images/%s.png'
      os.popen(output % (num, num))

   def clean_up(self):
      try:
         os.stat('tmp.aj')
         os.popen('rm tmp.aj')
      except:
         pass
