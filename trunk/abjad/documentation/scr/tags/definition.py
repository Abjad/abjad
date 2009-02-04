from tagparser import _TagParser


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
