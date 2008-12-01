#! /usr/bin/env python

import os
import re
import sys


class FileParser(object):

   def __init__(self, filename):
      self.filename = filename.strip('.raw')
      self.input = open(filename, 'r').readlines( )
      self.output =  [ ]
      self.tags = [SECTION( ), SUBSECTION( ), INTERFACE( ), DEFINITION( ),
         COMMENTS( ), TO_DO( ), CLASS_NAMES( ), 
         TOC_SECTION( ),
         LILY( ), ABJAD( )]

   @property
   def docType(self):
      result =  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
      result += ' "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n' 
      result += '<html xmlns="http://www.w3.org/1999/xhtml" '
      result += 'lang="en" xml:lang="en">\n\n'
      return result

   @property
   def footer(self):
      if 'css' in os.listdir(os.curdir):
         footer = 'index.html'
      elif 'css' in os.listdir(os.pardir):
         footer = '../index.html'
      elif 'css' in os.listdir(os.pardir + os.sep + os.pardir):
         footer = '../../index.html'
      elif 'css' in os.listdir(
         os.pardir + os.sep + os.pardir + os.sep + os.pardir):
         footer = '../../../index.html'
      else:
         raise ValueError('can not find index.html for footer.')
      result = '\n<p class="footer"><a href="%s">Contents</a></p>'
      result %= footer
      result += '\n\n</div>\n\n</body>\n\n</html>\n'
      return result

   @property
   def head(self):
      result  = '<head>\n\n'
      result += '<link rel="stylesheet" href="%s" type="text/css"/>'
      result %= self.stylesheet
      result += '\n\n'
      result += '<title>The Abjad Doc Site</title>\n\n'
      result += '</head>\n\n'
      return result

   def parse(self):
      partial = self.input
      for tag in self.tags:
         print "\nProcessing %s tag..." % tag.__class__.__name__
         tag.parse(partial)
         partial = tag.output
      self.output = partial
      self.writeOutput( )

   @property
   def stylesheet(self):
      if 'css' in os.listdir(os.curdir):
         stylesheet = 'css/abjad.css'
      elif 'css' in os.listdir(os.pardir):
         stylesheet = '../css/abjad.css'
      elif 'css' in os.listdir(os.pardir + os.sep + os.pardir):
         stylesheet = '../../css/abjad.css'
      elif 'css' in os.listdir(
         os.pardir + os.sep + os.pardir + os.sep + os.pardir):
         stylesheet = '../../../css/abjad.css'
      else:
         raise ValueError('can not find abjad.css stylesheet.')
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
         

class _TagParser(object):

   def __init__(self):
      self.output = [ ]

   def parse(self):
      pass


class SECTION(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<section>' in line:
            self.output.append(line.replace(
               '<section>', '<h2 class="page-section">').strip('\n')
               + '</h2>\n')
         else:
            self.output.append(line)


class SUBSECTION(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<subsection>' in line:
            name = line.replace('<subsection>', '')
            name = name.strip( )
            self.output.append('<div class="subsection">\n')
            if name.capitalize( ):
               self.output.append('\n')
               self.output.append('<h2>%s</h2>\n' % name.capitalize( )) 
         elif '</subsection>' in line:
            self.output.append('</div>\n')
         else:
            self.output.append(line)


class INTERFACE(_TagParser):

   def __init__(self):
      self.output = [ ]
      self.within = False

   def parse(self, lines):
      for line in lines:
         if '<interface>' in line:
            self.parse_open_interface(line)
         elif '</interface>' in line:
            self.parse_close_interface(line)
         elif self.open_block(line):
            self.parse_open_block(line)
         elif self.close_block(line):
            self.parse_close_block(line)
         elif '<local>' in line:
            self.parse_local_attribute(line)
         elif '<inherited>' in line:
            self.parse_inherited_attribute(line)
         else:
            self.output.append(line)

   def open_block(self, line):
      if '<attributes>' in line:
         return True
      elif '<dictionaries>' in line:
         return True
      elif '<methods>' in line:
         return True
      elif '<overloads>' in line:
         return True
      else:
         return False

   def close_block(self, line):
      if '</attributes>' in line:
         return True
      elif '</dictionaries>' in line:
         return True
      elif '</methods>' in line:
         return True
      elif '</overloads>' in line:
         return True
      else:
         return False

   def parse_open_interface(self, line):
      if self.within:
         print 'ERROR: unmatched <interface>.'
      else:
         self.within = True
         output = '<h2 class="page-section">Public interface</h2>\n'
         self.output.append(output)
         self.output.append('\n')
         self.output.append('<div class="interface">\n')

   def parse_close_interface(self, line):
      if not self.within:
         print 'ERROR: unmatched </interface>.'
      else:
         self.within = False
         self.output.append('</div>\n')

   def parse_open_block(self, line):
      if self.within:
         name = line.replace('<', '').replace('>', '')
         name = name.strip( )
         name = name.capitalize( )
         self.output.append('<div class="block">\n')
         output = '<div class="name">%s</div>\n' % name
         self.output.append(output)
      else:
         self.output.append(line)

   def parse_close_block(self, line):
      if self.within:
         self.output.append('</div>\n')
      else:
         self.output.append(line)

   def parse_local_attribute(self, line):
      if self.within:
         attribute = line.replace('<local>', '')
         attribute = attribute.strip( )
         output = '<div class="attribute">'
         output += '<div class="local">'
         output += '<a href="#%s">' % attribute
         output += '%s' % attribute
         output += '</a>'
         output += '</div>'
         output += '</div>\n'
         self.output.append(output)
      else:
         self.output.append(line)

   def parse_inherited_attribute(self, line):
      if self.within:
         attribute = line.replace('<inherited>', '')
         attribute = attribute.strip( )
         output = '<div class="attribute">'
         output += '<div class="inherited">'
         output += '<a href="#%s">' % attribute
         output += '%s' % attribute
         output += '</a>'
         output += '</div>'
         output += '</div>\n'
         self.output.append(output)
      else:
         self.output.append(line)


class DEFINITION(_TagParser):

   def __init__(self):
      self.output = [ ]
      self.within = False

   def parse(self, lines):
      for line in lines:
         if '<definition>' in line:
            self.parse_open_definition(line)
         elif '</definition>' in line:
            self.parse_close_definition(line)
         elif '<header>' in line:
            self.parse_open_header(line)
         elif '</header>' in line:
            self.parse_close_header(line)
         elif '<body>' in line:
            self.parse_open_body(line)
         elif '</body>' in line:
            self.parse_close_body(line)
         elif '<local>' in line:
            self.parse_local_attribute(line)
         elif '<inherited>' in line:
            self.parse_inherited_attribute(line)
         else:
            self.output.append(line)

   def parse_open_definition(self, line):
      if self.within:
         print 'ERROR: unmatched <definition>.'
      else:
         self.within = True
         self.output.append('<div class="definition">\n')

   def parse_close_definition(self, line):
      if not self.within:
         print 'ERROR: unmatched </definition>.'
      else:
         self.within = False
         self.output.append('</div>\n')

   def parse_open_header(self, line):
      if self.within:
         self.output.append('<div class="header">\n')
      else:
         self.output.append(line)

   def parse_close_header(self, line):
      if self.within:
         self.output.append('</div>\n')
      else:
         self.output.append(line)
   
   def parse_open_body(self, line):
      if self.within:
         self.output.append('<div class="body">\n')
      else:
         self.output.append(line)

   def parse_close_body(self, line):
      if self.within:
         self.output.append('</div>\n')
      else:
         self.output.append(line)

   def parse_local_attribute(self, line):
      if self.within:
         attribute = line.replace('<local>', '')
         attribute = attribute.strip( )
         output = '<div class="attribute">'
         output += '<div class="local">'
         output += '<a name="%s">' % attribute
         output += '%s' % attribute
         output += '</a>'
         output += '</div>'
         output += '</div>\n'
         self.output.append(output)
      else:
         self.output.append(line)

   def parse_inherited_attribute(self, line):
      if self.within:
         attribute = line.replace('<inherited>', '')
         attribute = attribute.strip( )
         output = '<div class="attribute">'
         output += '<div class="inherited">'
         output += '<a name="%s">' % attribute
         output += '%s' % attribute
         output += '</a>'
         output += '</div>'
         output += '</div>\n'
         self.output.append(output)
      else:
         self.output.append(line)


#class INTRODUCTION(_TagParser):
#
#   def parse(self, lines):
#      for line in lines:
#         if '<introduction>' in line:
#            self.output.append('<div class="introduction">\n')
#         elif '</introduction>' in line:
#            self.output.append('</div>\n')
#         else:
#            self.output.append(line)


class TOC_SECTION(_TagParser):

   def __init__(self):
      self.output = [ ]
      self.within = False

   def parse(self, lines):
      for line in lines:
         if '<toc-section>' in line:
            self.within = True
            self.output.append('<div class="toc-section">\n')
         elif '</toc-section>' in line:
            self.within = False
            self.output.append('</div>\n')
         elif '<header>' in line:
            if self.within:
               name = line.replace('<header>', '').strip( )
               output = '<h3>%s</h3>\n' % name
               self.output.append(output)
            else:
               self.output.append(line)
         elif '<body>' in line:
            if self.within:
               self.output.append('<div class="body">\n')
            else:
               self.output.append(line)
         elif '</body>' in line:
            if self.within:
               self.output.append('</div>\n')
            else:
               self.output.append(line)
         else:
            self.output.append(line)


class LILY(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<lily>' in line:
            self.output.append('<pre class="lilypond">\n')
         elif '</lily>' in line:
            self.output.append('</pre>\n')
         else:
            self.output.append(line)


class ABJAD(_TagParser):

   def __init__(self):
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
      tmp_aj.write("tmp_ly = open('%s.ly', 'w')\n" % self.cur_image_number)
      tmp_aj.write("""tmp_ly.write('\\\\version "2.11.56"\\n')\n""")
      tmp_aj.write("""tmp_ly.write('\\\\include "english.ly"\\n')\n""")
      tmp_aj.write(
         """tmp_ly.write('\\\\include "%s/scm/abjad.scm"\\n')\n""" % ABJADPATH)
      tmp_aj.write(
         """tmp_ly.write('\\\\include "%s/layout/web.ly"\\n')\n""" % ABJADPATH)
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


class COMMENTS(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<comments>' in line:
            self.output.append('<h2 class="page-section">Comments</h2>\n')
            self.output.append('\n')
            self.output.append('<div class="comments">\n')
         elif '</comments>' in line:
            self.output.append('</div>\n')
         else:
            self.output.append(line)


class TO_DO(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<to-do>' in line:
            self.output.append('<h2 class="page-section">To do</h2>\n')
            self.output.append('\n')
            self.output.append('<div class="to-do">\n')
         elif '</to-do>' in line:
            self.output.append('</div>\n')
         else:
            self.output.append(line)


class CLASS_NAMES(_TagParser):

   change = {
      '<_Accidental>' : 'accidental_class',
      '<assignability>' : 'assignability',
      '<_ArticulationsInterface>' : 'articulations_interface',
      '<_BarlineInterface>' : 'barline_interface',
      '<_BeamInterface>' : 'beam_interface',
      '<Chord>' : 'chord_class',
      '<_Clef>' : 'clef_class', 
      '<_ClefInterface>' : 'clef_interface',
      '<_Comments>' : 'comments_class',
      '<_Component>' : 'component_class',
      '<Container>' : 'container_class',
      '<_ContainerDurationInterface>' : 'container_duration_interface',
      '<_DotsInterface>' : 'dots_interface',
      '<_DurationInterface>' : 'duration_interface_class',
      '<duration token>' : 'duration_token',
      '<_DynamicsInterface>' : 'dynamics_interface',
      '<_FDTupletDurationInterface>' : 'fdtuplet_duration_interface_class',
      '<FixedDurationTuplet>' : 'fdtuplet_class',
      '<_FMTupletDurationInterface>' : 'fmtuplet_duration_interface_class',
      '<FixedMultiplierTuplet>' : 'fmtuplet_class',
      '<_GlissandoInterface>' : 'glissando_interface',
      '<_GraceInterface>' : 'grace_interface',
      '<_HarmonicInterface>' : 'harmonic_interface',
      '<_Leaf>' : 'leaf_class',
      '<_LeafDurationInterface>' : 'leaf_duration_interface_class',
      '<_LeafFormatter>' : 'leaf_formatter_class',
      '<_LeafSpannerInterface>' : 'leaf_spanner_interface',
      '<_MeasureDurationInterface>' : 'measure_duration_interface_class',
      '<Note>' : 'note_class',
      '<_NoteHead>' : 'notehead_class',
      '<notehead token>' : 'notehead_token',
      '<Pitch>' : 'pitch_class',
      '<_PitchTools>' : 'pitch_tools',
      '<pitch token>' : 'pitch_token',
      '<Rational>' : 'rational_class',
      '<Rest>' : 'rest_class',
      '<Skip>' : 'skip_class',
      '<_Staff>' : 'staff_class',
      '<_StemInterface>' : 'stem_interface',
      '<_TempoInterface>' : 'tempo_interface',
      '<tempo token>' : 'tempo_token',
      '<_TieInterface>' : 'tie_interface',
      '<_TremoloInterface>' : 'tremolo_interface',
      '<_TrillInterface>' : 'trill_interface',
      '<_TupletDurationInterface>' : 'tuplet_duration_interface_class',
      '<Voice>' : 'voice_class',
   }

   def parse(self, lines):
      for line in lines:
         for key in self.change.keys( ):
            if key in line:
               directory_name = self.change[key]
               class_name = key[1 : -1]
               ### TODO: fix relative URL to work at different level
               ###       of doc site
               target = '<code><a href="../%s/index.html">%s</a></code>'
               target %= (directory_name, class_name)
               line = line.replace(key, target)
         self.output.append(line)


#### EXECUTABLE ####

ABJADPATH = os.environ['ABJADPATH']

if __name__ == '__main__':

   fileparser = FileParser(sys.argv[1])

   fileparser.parse( )
