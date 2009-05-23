from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _BarLineInterface(_Interface, _GrobHandler):
   '''Abjad _BarLineInterface manages the LilyPond BarLine grob.
      One public read / write 'kind' attribute.
      Makes format contribution at container closing or after leaf.'''
   
   def __init__(self, _client):
      '''Bind to client and set ``kind`` to ``None``.'''
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'BarLine')
      self._kind = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      '''Format contribution at container closing or after leaf.'''
      result = [ ]
      if self.kind:
         result.append(r'\bar "%s"' % self.kind)
      return result

   @apply
   def kind( ):
      '''Kind of barline, from LilyPond documentation.'''
      def fget(self):
         return self._kind
      def fset(self, expr):
         self._kind = expr
      return property(**locals( ))
