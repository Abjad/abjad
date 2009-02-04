from tagparser import _TagParser


class SECTION(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<section>' in line:
            self.output.append(line.replace(
               '<section>', '<h2 class="page-section">').strip('\n')
               + '</h2>\n')
         else:
            self.output.append(line)
