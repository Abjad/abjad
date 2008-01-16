def hasname(instance, classname):
   x = instance.__class__
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
      raise ValueError('classname be must a str or tuple of str.')
   return False
