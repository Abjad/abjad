from grace import Grace
from .. helpers.hasname import hasname


class GraceInterface(object):

   def __init__(self):
      self._before = None
      self._after = None
   
   @apply
   def before( ):
      def fget(self):
         return self._before
      def fset(self, arg):
         if arg == None:
            self._before = None
         elif isinstance(arg, Grace):
            self._before = arg
         elif hasname(arg, 'Leaf'):
            self._before = Grace([arg])
         elif isinstance(arg, list):
            self._before = Grace(arg)
         elif arg in ('grace', 'acciaccatura', 'appoggiatura'):
            assert self._before
            self._before._type = arg
         else:
            raise ValueError('can not set before.')
      return property(**locals( ))

   @apply
   def after( ):
      def fget(self):
         return self._after
      def fset(self, arg):
         if arg == None:
            self._after = None
         else:
            if isinstance(arg, Grace):
               self._after = arg
            elif hasname(arg, 'Leaf'):
               self._after = Grace([arg])
            elif isinstance(arg, list):
               self._after = Grace(arg)
            else:
               raise ValueError('can not set after.')
            self._after._type = 'after'
      return property(**locals( ))
