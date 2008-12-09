from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _MarkupInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._down = [ ]
      self._up = [ ]

   ### PRIVATE ATTRIBUTES ###

   @property
   def _right(self):
      result = [ ]
      for markup in self.up:
         result.append('^ \markup { %s }' % str(markup))
      for markup in self.down:
         result.append('_ \markup { %s }' % str(markup))
      return result

   ### PUBLIC ATTRIBUTES ###

   @apply
   def down( ):
      def fget(self):
         return self._down
      return property(**locals( ))

   @apply
   def up( ):
      def fget(self):
         return self._up
      return property(**locals( ))
