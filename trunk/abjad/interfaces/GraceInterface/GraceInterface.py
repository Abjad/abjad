from abjad.interfaces._Interface import _Interface


class GraceInterface(_Interface):

   def __init__(self, client):
      from abjad.tools.gracetools import Grace
      _Interface.__init__(self, client)
      self.before = Grace( )
      self.after = Grace( )
   
   ## PRIVATE METHODS ##

   def _establish_after(self):
      self.after._carrier = self._client

   def _establish_before(self):
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
         from abjad.components._Leaf import _Leaf
         from abjad.tools.gracetools import Grace
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
         self._establish_after( )
      return property(**locals( ))

   @apply
   def before( ):
      '''Grace music before leaf.'''
      def fget(self):
         return self._before
      def fset(self, arg):
         from abjad.components._Leaf import _Leaf
         from abjad.tools.gracetools import Grace
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
         self._establish_before( )
      return property(**locals( ))
