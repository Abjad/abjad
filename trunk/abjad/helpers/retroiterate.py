from abjad.helpers.hasname import hasname


def retroiterate(expr, classname):
   '''
   Returns a generator that iterates backwards collecting all instances 
   with class name <clasname> found in the given <expr> structure.
   '''
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
