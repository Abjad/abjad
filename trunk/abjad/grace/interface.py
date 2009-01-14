#from abjad.core.abjadcore import _Abjad
from abjad.core.interface import _Interface
from abjad.grace.grace import Grace
from abjad.helpers.hasname import hasname


class _GraceInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self.before = Grace( )
      self.after = Grace( )

   def _establishBefore(self):
      self.before._parent = self._client

   def _establishAfter(self):
      self.after._parent = self._client


   ### PUBLIC ATTRIBUTES ###
   
   @apply
   def before( ):
      def fget(self):
         return self._before
      def fset(self, arg):
         if arg is None:
            self._before = Grace( )
            #self._before.type = 'grace'
         elif isinstance(arg, Grace):
            self._before = arg
         elif hasname(arg, '_Leaf'):
            self._before = Grace([arg])
         elif isinstance(arg, list):
            self._before = Grace(arg)
         elif arg in ('grace', 'acciaccatura', 'appoggiatura'):
            self._before.type = arg
         else:
            raise ValueError('can not set before.')
         self._establishBefore( )
      return property(**locals( ))

   @apply
   def after( ):
      def fget(self):
         return self._after
      def fset(self, arg):
         if arg is None:
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
         self._establishAfter( )
      return property(**locals( ))
