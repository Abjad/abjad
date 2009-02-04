from tagparser import _TagParser


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
