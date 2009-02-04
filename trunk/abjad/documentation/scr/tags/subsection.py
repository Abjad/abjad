from tagparser import _TagParser


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
