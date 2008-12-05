def _my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def _load_classes(forbid_list):
   import os
   for root, dirs, files in os.walk(__path__[0]):
      root = root[root.rindex('abjad'):]
      if root == 'abjad':
         # skip over any stray abjad/*.py files at root level!
         pass
      else:
         for file in files:
            if file.endswith('py') and not file.startswith(('_', '.')):
               if all([y not in root for y in forbid_list]):
                  module = '.'.join([root.replace(os.sep, '.'), file[:-3]])
                  for key, value in _my_import(module).__dict__.items( ):
                     if getattr(value, '__module__', None) == module:
                        globals( )[key] = value

def _remove_modules():
   from types import ModuleType
   for key, value in globals().items():
      if isinstance(value, ModuleType) and not key.startswith('_'):
         globals().pop(key)

#_load_classes(('svn', 'tools', 'wf', 'test', 'checks'))
_load_classes(('documentation', 'svn', 'tools', 'test', 'checks'))
print 'loaded classes'
_remove_modules()
print 'removed modules'
