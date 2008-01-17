def f(expr):
   if hasattr(expr, 'format'):
      print expr.format
   elif isinstance(expr, list):
      for x in expr:
         print x.format
   else:
      raise ValueError('must be score component or list.')
