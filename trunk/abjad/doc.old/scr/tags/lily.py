from tagparser import _TagParser


class LILY(_TagParser):

   def parse(self, lines):
      for line in lines:
         if '<lily>' in line:
            self.output.append('<pre class="lilypond">\n')
         elif '</lily>' in line:
            self.output.append('</pre>\n')
         else:
            self.output.append(line)
