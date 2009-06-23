from tagparser import _TagParser


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
