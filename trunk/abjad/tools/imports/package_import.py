from abjad.tools.imports.get_functions_in_module import _get_functions_in_module
import os

def _package_import(path, namespace):
   '''Non-recursive import helper. 
   All packages (non-leaf sub-modules) in `path` are imported to the 
   given `namespace`.
   All the functions and classes inside modules (leaf-modules, *.py files) 
   found in `path` are imported into `namespace`.'''
   module = path[path.rindex('abjad'):]
   module = module.replace(os.sep, '.')

   for element in os.listdir(path):
      if os.path.isfile(os.path.join(path, element)):
         if not element.startswith('_') and element.endswith('.py'):
            ## import function inside module
            submod = os.path.join(module, element[:-3])
            functions = _get_functions_in_module(submod)
            for f in functions:
               namespace[f.__name__] = f

      elif os.path.isdir(os.path.join(path, element)):
         if not element in ('.svn', 'test'):
            #exec('from %s import %s' % (module, element))
            submod = '.'.join([module, element])
            namespace[element] = __import__(submod, fromlist =['*'])
      else:
         print 'Not a dir, not a file, what is %s?' % element

   del(namespace['_package_import'])
