from abjad.core.interface import _Interface
from abjad.grace.grace import Grace


class _GraceInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self.before = Grace( )
      self.after = Grace( )
   
   ## PRIVATE METHODS ##

   def _establishAfter(self):
      self.after._carrier = self._client

   def _establishBefore(self):
      '''Replaced _parent with _carrier because the 
         navigation code assumes that a _parent is a Container 
         and thus has a _music list.
         This is not the case for Leaves.'''
      self.before._carrier = self._client

   ## PUBLIC ATTRIBUTES ##
   
   @apply
   def after( ):
      '''Grace before after leaf.'''
      def fget(self):
         return self._after
      def fset(self, arg):
         from abjad.leaf.leaf import _Leaf
         if arg is None:
            self._after = Grace( )
         else:
            if isinstance(arg, Grace):
               self._after = arg
            elif isinstance(arg, _Leaf):
               self._after = Grace([arg])
            elif isinstance(arg, list):
               self._after = Grace(arg)
            else:
               raise ValueError('can not set after.')
         self._after.kind = 'after'
         self._establishAfter( )
      return property(**locals( ))

   @apply
   def before( ):
      '''Grace music before leaf.'''
      def fget(self):
         return self._before
      def fset(self, arg):
         from abjad.leaf.leaf import _Leaf
         if arg is None:
            self._before = Grace( )
         elif isinstance(arg, Grace):
            self._before = arg
         elif isinstance(arg, _Leaf):
            self._before = Grace([arg])
         elif isinstance(arg, list):
            self._before = Grace(arg)
         elif arg in ('grace', 'acciaccatura', 'appoggiatura'):
            self._before.kind = arg
         else:
            raise ValueError('can not set before.')
         self._establishBefore( )
      return property(**locals( ))
