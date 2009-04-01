def iterate_grace(expr, klass):
   if hasattr(expr, 'grace'):
      for m in expr.grace.before:
         for x in iterate_grace(m, klass):
            yield x
      if isinstance(expr, klass):
         yield expr
      for m in expr.grace.after:
         for x in iterate_grace(m, klass):
            yield x
   elif isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in iterate_grace(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in iterate_grace(m, klass):
            yield x
