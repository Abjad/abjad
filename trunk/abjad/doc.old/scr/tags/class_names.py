from tagparser import _TagParser
import os


class CLASS_NAMES(_TagParser):

   from class_name_substitutions import change

   def parse(self, lines):
      for line in lines:
         for key in self.change.keys( ):
            if key in line:
               directory_name = self.change[key]
               class_name = key[1 : -1]
               target = '<code><a href="%s/%s/index.html">%s</a></code>'
               target %= (
                  os.sep.join(
                     ['..'] * (self.depth - 1)), directory_name, class_name)
               line = line.replace(key, target)
         self.output.append(line)
