from interface import _Interface

class ClassInspector(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Inspector')

#   def inheritence(self, arg):
#      result = [arg.__class__.__name__]
#      i = 1
#      while True:
#         parent = eval(
#            'arg.__class__.%s.__name__' % '.'.join(['__base__'] * i))
#         if parent == 'object':
#            break
#         else:
#            result.append(parent)
#            i += 1
#      return result   

   def _has(self, classname):
      x = self._client.__class__
      if isinstance(classname, str):
         while x is not None:
            if x.__name__ is classname:
               return True
            else:
               x = x.__base__
      elif isinstance(classname, tuple):
         while x is not None:
            if x.__name__ in classname:
               return True
            else:
               x = x.__base__
      else:
         raise ValueError('be must a classname string or tuple of strings.')
      return False
