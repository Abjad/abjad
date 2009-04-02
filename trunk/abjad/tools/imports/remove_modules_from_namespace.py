from types import ModuleType

def _remove_modules_from_namespace(namespace):
   for key, value in namespace.items( ):
      if isinstance(value, ModuleType) and not key.startswith('_'):
         #namespace.pop(key)
         del(namespace[key])
