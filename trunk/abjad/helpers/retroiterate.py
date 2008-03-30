from abjad.helpers.hasname import hasname

def retroiterate(expr, classname):
   if hasname(expr, classname):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in reversed(expr):
         for x in retroiterate(m, classname):
            yield x
   if hasattr(expr, '_music'):
      for m in reversed(expr._music):
         for x in retroiterate(m, classname):
            yield x

   
