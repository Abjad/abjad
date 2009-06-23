from tagparser import _TagParser


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
