from abjad.book.parser.tagparser import _TagParser
import os
import subprocess
import sys


class _AbjadTag(_TagParser):
   def __init__(self, lines):
      _TagParser.__init__(self, lines)
      self._close_tag = '</abjad>'
      self._open_tag = '<abjad>'
      self._target_open_tag = '<pre class="abjad">\n'
      self._target_close_tag = '</pre>\n'
      self._abjad_code = ['from abjad import *\n']
      self._image_tag = '<img alt="" src="images/%s.png"/>\n'
      self._images_collected = [ ]


   def process(self):
      self._verifyTag( )
      self._parse( )
      self._runAbjadCode( )
      return self.output


   def _parse(self):
      in_block = False
      for line in self._input:
         if self._open_tag in line:
            self.output.append(self._target_open_tag)
            in_block = True 
         elif self._close_tag in line:
            self.output.append(self._target_close_tag)
            in_block = False
            if len(self._images_collected) > 0:
               while len(self._images_collected) > 0:
                  self.output.append(self._images_collected.pop(0))
         elif in_block:
            self._handle_internal_line(line)
         else:
            self.output.append(line)


   def _handle_internal_line(self, line):
      if not 'hide>' in line:
         self.output.append(line)

      if 'abjad>' in line:
         abjad_directive = line.replace('abjad>', '').strip( )
      elif 'hide> ' in line:
         abjad_directive = line.replace('hide>', '').strip( )
      elif '>>> ' in line:
         abjad_directive = line.replace('>>>', '').strip( )
      else:
         abjad_directive = None

      if abjad_directive:
         if not abjad_directive.startswith('show'):
            self._abjad_code.append(abjad_directive)

         if abjad_directive.startswith('write'):
            image_name = abjad_directive.split(',')[1]
            image_name = image_name.strip(' ').rstrip(')').strip("'")
            image = self._image_tag % image_name
            self._images_collected.append(image)


   def _makeImages(self):
      for file in os.listdir(os.curdir):
         if file.endswith('.ly'):
            file_base = file.rstrip('.ly')
            # NOTE: setting stderr = sys.stderr 
            # below will print LilyPond messages
            p = subprocess.Popen(
               'lilypond --png -dresolution=300 %s' % file,
               shell = True, stdout = subprocess.PIPE, 
               stderr = subprocess.PIPE)
            p.communicate( )
            ## NOTE: why popen and not system here?
            output = 'convert %s.png -trim -resample 40%% %s.png'
            os.popen(output % (file_base, file_base))


   def _runAbjadCode(self):
      def _createTempDirectory( ):
         if not os.path.isdir('tmp_out'):
            os.mkdir('tmp_out')

      def _createImagesDirectory( ):
         if not os.path.isdir('images'):
            os.mkdir('images')

      ## write abjad code to file
      _createTempDirectory( )
      os.chdir('tmp_out')
      f = open('tmp_abjad.aj', 'w')
      f.writelines('\n'.join(self._abjad_code))
      f.close( )
      ## run it.
      os.system('python tmp_abjad.aj')
      self._makeImages( )
      os.chdir('..')
      _createImagesDirectory( ) 
      os.system('mv tmp_out/*.png images')
      os.system('rm -r tmp_out')

