import os

def _get_topmost_module(name):
   '''Return the topmost module from a hierarchy of package/modules. 
   The passed argument 'name' should describe the full package/module1/module2 
   directory structure pointing to the module you want returned (module2). 
   Example:
   _get_topmost_module('abjad.helpers.construct')
   returns the 'construct' module.'''
   name = mod.replace(os.sep, '.')
   mod = __import__(name)
   components = name.split('.')
   for comp in components[1:]:
      mod = getattr(mod, comp)
   return mod



