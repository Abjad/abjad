from grace import Grace
from .. helpers.hasname import hasname


class _GraceInterface(object):

   def __init__(self):
      #self._before = None
      #self._after = None
      self.before = Grace( )
      self.after = Grace( )
   
   @apply
   def before( ):
      def fget(self):
         return self._before
      def fset(self, arg):
         if arg == None:
            #self._before = None
            self._before = Grace( )
            self._before.type = 'grace'
         elif isinstance(arg, Grace):
            self._before = arg
         elif hasname(arg, '_Leaf'):
            self._before = Grace([arg])
         elif isinstance(arg, list):
            self._before = Grace(arg)
         elif arg in ('grace', 'acciaccatura', 'appoggiatura'):
            #assert self._before
            self._before.type = arg
         else:
            raise ValueError('can not set before.')
      return property(**locals( ))

   @apply
   def after( ):
      def fget(self):
         return self._after
      def fset(self, arg):
         if arg == None:
            #self._after = None
            self._after = Grace( )
         else:
            if isinstance(arg, Grace):
               self._after = arg
            elif hasname(arg, '_Leaf'):
               self._after = Grace([arg])
            elif isinstance(arg, list):
               self._after = Grace(arg)
            else:
               raise ValueError('can not set after.')
         self._after.type = 'after'
      return property(**locals( ))
