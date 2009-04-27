from abjad.book.parser.tagparser import _TagParser
import os
import re
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


   def process(self):
      ## create temp directory to work in
      _createDirectory('tmp_out')
      os.chdir('tmp_out')

      ## start processing
      self._verifyTag( )
      self._parse( )
      rendered = self._renderImages( )
      
      ## clean up directories
      os.chdir('..')
      if rendered: 
         _createDirectory('images') 
         os.system('mv tmp_out/*.png images')
      os.system('rm -r tmp_out')
      return self.output


   ## PRIVATE METHODS ##

   def _parse(self):
      print 'Parsing file...'
      input = self._input[:]
      while len(input) > 0:
         code, type = self._get_next_code_block(input)
         if code:
            output_codeblock, images = self._handle_code_block(code, type)
            if output_codeblock:
               self.output.append(self._target_open_tag)
               self.output.extend(output_codeblock)
               self.output.append(self._target_close_tag)
            if images:
               for image in images:
                  self.output.append(self._image_tag % image)


   def _get_next_code_block(self, input):
      result = [ ]
      type = None
      in_block = False
      for line in input[:]:
         input.remove(line) 
         if self._open_tag in line:
            in_block = True
            if 'hide=true' in line.replace(' ', '').lower( ):
               type = 'hide'
         elif self._close_tag in line:
            return result, type
         elif in_block:
            result.append(line)
         else:
            self.output.append(line)
      return None, None

   def _handle_code_block(self, lines, type):
      lines = [line.replace('\n', '') for line in lines]
      code, images = self._parse_code_block(lines, type)
      self._abjad_code.extend(code)
      out = _execute_abjad_code(self._abjad_code)
      out = _extract_code_block(out)
      out = _recover_commented_show_directives(out)
      out = _remove_hidden_directives(out)
      out = _insert_abjad_prompt(out, lines)
      return [line + '\n' for line in out], images


   def _renderImages(self):
      rendered_image = False
      for file in os.listdir(os.curdir):
         print 'Rendering "%s"...' % file
         if file.endswith('.ly'):
            file_base = file.rstrip('.ly')
            # NOTE: setting stderr = sys.stderr 
            # below will print LilyPond messages
            p = subprocess.Popen(
               'lilypond --png -dresolution=300 %s' % file,
               shell = True, stdout = subprocess.PIPE, 
               stderr = subprocess.PIPE)
            out, err = p.communicate( )
            ## NOTE: why popen and not system here?
            output = 'convert %s.png -trim -resample 40%% %s.png'
            os.popen(output % (file_base, file_base))
            rendered_image = True
      return rendered_image


   def _parse_code_block(self, lines, type):
      '''Parses code and adds it to self._abjad_code. 
      Returns names of images found.'''
      images = [ ]
      code = [ ]
      ## handle code block type
      if type == 'hide':
         for i in range(len(lines)):
            lines[i] += '<hide'

      code.append('print "## START ##"')
      for line in lines:
         ## get indentation
         indent = re.search('^ +', line)
         if indent:
            indent = indent.group( )

         ## get abjad directive 
         if '<hide' in line:
            abjad_directive = line.replace('<hide', '#<hide')
         else:
            abjad_directive = line

         ## handle abjad directive
         if 'show(' in abjad_directive:
            abjad_directive = '%s#abjad_comment#%s' % ((indent or ''), 
               abjad_directive)
         
         code.append("%sprint '''%s'''" % ((indent or ''), abjad_directive))
         code.append(abjad_directive)

         ## handle and collect images
         if abjad_directive.startswith('write'):
            images.append(_get_image_name(abjad_directive))

      return code, images


## HELPERS ##

def _insert_abjad_prompt(output_lines, input_lines):
   result = [ ]
   for oline in output_lines:
      if oline in input_lines:
         oline = 'abjad> ' + oline
      result.append(oline)
   return result
      
def _get_image_name(directive):
   try:
      image_name = directive.split(',')[1].split(')')[0]
      image_name = image_name.strip(' ').strip("'").strip('"')
      return image_name
   except IndexError:
      print "Problem parsing 'write( )'. Did you forget to add a file name?"

def _remove_hidden_directives(lines):
   '''remove hidden lines'''
   for line in lines[:]:
      if '#<hide' in line:
         lines.remove(line)
   return lines

def _recover_commented_show_directives(lines):
   ''' remove #abjad_comments# from temporarily commented show( ).'''
   for i, line in enumerate(lines):
      if line.startswith('#abjad_comment#'):
         lines[i] = line.strip('#abjad_comment#')
   return lines

def _extract_code_block(lines):
   for i, line in enumerate(reversed(lines)):
      if line == '## START ##':
         del(lines[0: -i])
         break
   return lines

def _execute_abjad_code(lines):
   p = subprocess.Popen('python', stdin = subprocess.PIPE, 
      stdout = subprocess.PIPE, stderr = subprocess.PIPE)
   out, err = p.communicate('\n'.join(lines))
   if err:
      print "\nERROR in Abjad script compilation:"
      print err
      sys.exit(2)
   out = out.split('\n')
   return out

def _createDirectory(dir):
   if not os.path.isdir(dir):
      os.mkdir(dir)


## OLD VERSION ##
#class _AbjadTag(_TagParser):
#   def __init__(self, lines):
#      _TagParser.__init__(self, lines)
#      self._close_tag = '</abjad>'
#      self._open_tag = '<abjad>'
#      self._target_open_tag = '<pre class="abjad">\n'
#      self._target_close_tag = '</pre>\n'
#      self._abjad_code = ['from abjad import *\n']
#      self._image_tag = '<img alt="" src="images/%s.png"/>\n'
#      self._images_collected = [ ]
#
#
#   def process(self):
#      self._verifyTag( )
#      self._parse( )
#      self._runAbjadCode( )
#      return self.output
#
#
#   ## PRIVATE METHODS ##
#
#   def _parse(self):
#      print 'Parsing file...'
#      input = self._input[:]
#      while len(input) > 0:
#         code = self._get_next_code_block(input)
#         if code:
#            output_codeblock = self._handle_code_block(code)
#            if output_codeblock:
#               self.output.append(self._target_open_tag)
#               self.output.extend(output_codeblock)
#               self.output.append(self._target_close_tag)
#            if len(self._images_collected) > 0:
#               while len(self._images_collected) > 0:
#                  self.output.append(self._images_collected.pop(0))
#
#
#   def _get_next_code_block(self, input):
#      result = [ ]
#      in_block = False
#      for line in input[:]:
#         input.remove(line) 
#         if self._open_tag in line:
#            in_block = True
#         elif self._close_tag in line:
#            return result
#         elif in_block:
#            result.append(line)
#         else:
#            self.output.append(line)
#
#
#   def _handle_code_block(self, lines):
#      result = [ ]
#      for line in lines:
#         if not 'hide>' in line:
#            result.append(line)
#         ## get abjad directive 
#         if 'abjad>' in line:
#            abjad_directive = line.replace('abjad>', '').strip( )
#         elif 'hide> ' in line:
#            abjad_directive = line.replace('hide>', '').strip( )
#         elif '>>> ' in line:
#            abjad_directive = line.replace('>>>', '').strip( )
#         else:
#            abjad_directive = None
#         ## handle abjad directive
#         if abjad_directive:
#            if not abjad_directive.startswith('show'):
#               self._abjad_code.append(abjad_directive)
#            ## handle and collect images
#            if abjad_directive.startswith('write'):
#               try:
#                  image_name = abjad_directive.split(',')[1]
#                  image_name = image_name.strip(' ').rstrip(')').strip("'")
#                  image = self._image_tag % image_name
#                  self._images_collected.append(image)
#               except IndexError:
#                  print "write( ) function must be given a file name!"
#      return result 
#
#
#   def _makeImages(self):
#      print 'Rendering score images with LilyPond...'
#      for file in os.listdir(os.curdir):
#         if file.endswith('.ly'):
#            file_base = file.rstrip('.ly')
#            # NOTE: setting stderr = sys.stderr 
#            # below will print LilyPond messages
#            p = subprocess.Popen(
#               'lilypond --png -dresolution=300 %s' % file,
#               shell = True, stdout = subprocess.PIPE, 
#               stderr = subprocess.PIPE)
#            p.communicate( )
#            ## NOTE: why popen and not system here?
#            output = 'convert %s.png -trim -resample 40%% %s.png'
#            os.popen(output % (file_base, file_base))
#
#
#   def _runAbjadCode(self):
#      def _createTempDirectory( ):
#         if not os.path.isdir('tmp_out'):
#            os.mkdir('tmp_out')
#
#      def _createImagesDirectory( ):
#         if not os.path.isdir('images'):
#            os.mkdir('images')
#
#      ## write abjad code to file
#      _createTempDirectory( )
#      os.chdir('tmp_out')
#      f = open('tmp_abjad.aj', 'w')
#      f.writelines('\n'.join(self._abjad_code))
#      f.close( )
#      ## run it.
#      p = subprocess.Popen('python tmp_abjad.aj', shell = True, 
#         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#      out, error =  p.communicate( )
#      if error:
#         #raise SyntaxError(error)
#         print "\nERROR in Abjad script compilation:"
#         print error
#         os.chdir('..')
#         os.system('rm -r tmp_out')
#      else:
#         self._makeImages( )
#         os.chdir('..')
#         _createImagesDirectory( ) 
#         os.system('mv tmp_out/*.png images')
#         os.system('rm -r tmp_out')
#
