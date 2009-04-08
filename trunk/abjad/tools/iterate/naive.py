def naive(expr, klass):
   if isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in naive(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in naive(m, klass):
            yield x
