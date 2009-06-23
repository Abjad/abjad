from tagparser import _TagParser


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
