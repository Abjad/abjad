from abjad.helpers.hasname import hasname


def iterate(expr, classname):
   if hasname(expr, classname):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in iterate(m, classname):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in iterate(m, classname):
            yield x


def components(expr):
   return iterate(expr, '_Component')
