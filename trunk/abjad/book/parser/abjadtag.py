from abjad.book.parser.codeblock import _CodeBlock
from abjad.book.parser.tagparser import _TagParser
import os
import shutil
import subprocess
import sys


class _AbjadTag(_TagParser):

   def __init__(self, lines, skip_rendering = False):
      _TagParser.__init__(self, lines)
      self.skipRendering = skip_rendering
      self._close_tag = '</abjad>'
      self._open_tag = '<abjad>'
      self._target_open_tag = '<pre class="abjad">' + os.linesep
      self._target_close_tag = '</pre>' + os.linesep
      self._abjad_code = ['from abjad import *' + os.linesep]
      self._image_tag = '<img alt="" src="images/%s.png"/>' + os.linesep


   def process(self):
      self._verifyTag( )

      ## create temp directory to work in
      _create_directory('tmp_out')
      os.chdir('tmp_out')

      ## start processing
      self._parse( )

      if self.skipRendering:
         print 'Skipped image rendering by request.'
      else:
         self._renderImages( )
      
      ## clean up directories
      os.chdir('..')
      _create_directory('images') 
      for element in os.listdir('tmp_out'):
         #if element.endswith('.png'):
         if element[-4:] in ('.png', '.pdf'):
            shutil.move(os.path.join('tmp_out', element), 'images')
      shutil.rmtree('tmp_out')

      return self.output


   ## PRIVATE METHODS ##

   def _parse(self):
      print 'Parsing file...'
      input = self._input[:]
      while len(input) > 0:
         codeblock = self._get_next_code_block(input)
         if codeblock:
            self._handle_code_block(codeblock)
            if codeblock.finalOutputCode:
               self.output.append(self._target_open_tag)
               self.output.extend(codeblock.finalOutputCode)
               self.output.append(self._target_close_tag)
            if codeblock.images:
               for image in codeblock.images:
                  self.output.append(self._image_tag % image)


   def _get_next_code_block(self, input):
      result = _CodeBlock( )
      result.type = None
      in_block = False
      for line in input[:]:
         input.remove(line) 
         if self._open_tag in line:
            in_block = True
            result.type = self._get_block_type_from_open_tag(line)
         elif self._close_tag in line:
            return result
         elif in_block:
            result.preProcessedCode.append(line)
         else:
            self.output.append(line + os.linesep)
      return None


   def _get_block_type_from_open_tag(self, line):
      if 'hide=true' in line.replace(' ', '').lower( ):
         return 'hide'


   def _handle_code_block(self, codeblock):
      self._abjad_code.extend(codeblock.toProcessCode)
      out = _execute_abjad_code(self._abjad_code)
      codeblock.postProcessedCode = _extract_code_block(out)
      codeblock._collectImages( )


   def _renderImages(self):
      for file in os.listdir(os.curdir):
         if file.endswith('.ly'):
            print 'Rendering "%s"...' % file
            if 'latex' in self.__class__.__name__.lower( ):
               self._renderPDFimage(file)
            else:
               self._renderPNGimage(file)


   def _renderPDFimage(self, filename):
      file_base = filename.replace('.ly', '')
      p = subprocess.Popen('lilypond  %s' % filename,
         shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      out, err = p.communicate( )
      output = 'pdfcrop %s.pdf %s.pdf'
      os.popen(output % (file_base, file_base))


   def _renderPNGimage(self, filename):
      file_base = filename.replace('.ly', '')
      p = subprocess.Popen('lilypond --png -dresolution=300 %s' % filename,
         shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      out, err = p.communicate( )
      ## NOTE: why popen and not system here?
      output = 'convert %s.png -trim -resample 40%% %s.png'
      os.popen(output % (file_base, file_base))


## HELPERS ##

def _create_directory(dir):
   if not os.path.isdir(dir):
      os.mkdir(dir)


def _extract_code_block(lines):
   for i, line in enumerate(reversed(lines)):
      if line == '## START ##':
         del(lines[0: -i])
         break
   return lines


def _execute_abjad_code(lines):
   p = subprocess.Popen('python', stdin = subprocess.PIPE, 
      stdout = subprocess.PIPE, stderr = subprocess.PIPE)
   out, err = p.communicate(os.linesep.join(lines))
   if err:
      print os.linesep + "ERROR in Abjad script compilation:"
      print err
      sys.exit(2)
   #out = out.split('\n')
   out = out.splitlines( )
   return out

