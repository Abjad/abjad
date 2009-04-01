import os


def _get_functions_in_module(module_file):
   '''Collects and returns all functions defined in module_file.'''
   result = [ ]
   module_file = module_file.replace(os.sep, '.')
   mod = __import__(module_file, fromlist=['*'])
   for key, value in mod.__dict__.items( ):
      if not key.startswith('_'): ## if not a private function...
         if getattr(value, '__module__', None) == module_file:
            #print '"%s" in module %s ' % (key, module_file)
            result.append(value)
   return result

