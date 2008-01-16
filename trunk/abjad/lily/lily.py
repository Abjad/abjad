### TODO - grab COMMANDFILE and WORKDIR from cfg/abjad.cfg ###

from .. container.container import Container

class Lily(Container):
   '''TODO remove paper, layout, header altogether.'''

   def __init__(self, music, name = '', 
      includes = [], paper = [], layout = [], header = []):
   
      self.name = name
      self.includes = includes
      self.paper = paper
      self.layout = layout
      self.header = header
      Container.__init__(self, music)

      self.includes.insert(0, 'english.ly')
      self.includes.insert(1, COMMANDFILE)

   def __repr__(self):
      
      result = ['music']
      if len(self.includes) > 0:
         result.append('includes')
      if len(self.layout) > 0:
         result.append('layout')
      if len(self.paper) > 0:
         result.append('paper')
      if len(self.header) > 0:
         result.append('header')
      return 'LILY (%s)' % ', '.join(result)

   def setLayoutFile(self, fileName):
      self.includes.append(WORKDIR + fileName)

   @property
   def format(self):
   
      result = [ ]
      result.append(r'\version "%s"' % version + '\n')

      if len(self.includes) > 0:
         result.extend([r'\include "%s"' % i for i in self.includes])
         result.append('')

      if len(self.paper) > 0:
         result.append(r'\paper {')
         result.extend(['\t' + p for p in self.paper])
         result.append('}')
         result.append('')

      if len(self.layout) > 0:
         result.append(r'\layout {')
         result.extend(['\t' + l for l in self.layout])
         result.append('}')
         result.append('')

      if len(self.header) > 0:
         result.append(r'\header {')
         result.extend(['\t' + h for h in self.header])
         result.append('}')
         result.append('')

      if len(self) > 0:
         contents = [m.format + '\n' for m in self][0]
         if contents[0] == '\n':
            contents = contents[1:]
         result.append(contents)

      return '\n'.join(result)
