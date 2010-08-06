from abjad.cfg.cfg import ABJADPATH
import os


def _get_all_abjad_modules( ):
   '''Return a list of all Abjad modules.
   Exclude initializers and other modules beginning in double underscore.
   '''

   modules = [ ]
   for current_root, dirs, files in os.walk(ABJADPATH):
      if '.svn' not in current_root:
         if 'test' not in current_root:
            for file in files:
               if file.endswith('.py'):
                  if not file.startswith('__'):
                     module = os.path.join(current_root, file)
                     modules.append(module)
   return modules
   

if __name__ == '__main__':
   modules = _get_all_abjad_names( )
   for x in modules:
      print x
