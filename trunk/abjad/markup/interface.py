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
      if len(self.up) == 1:
         result.append(r'^ \markup { %s }' % str(self.up[0]))
      elif len(self.up) > 1:
         column = r'^ \markup { \column { %s } }' 
         column %= ' '.join([str(x) for x in self.up])
         result.append(column)
      if len(self.down) == 1:
         result.append(r'_ \markup { %s }' % str(self.down[0]))
      elif len(self.down) > 1:
         column = r'_ \markup { \column { %s } }' 
         column %= ' '.join([str(x) for x in self.down])
         result.append(column)
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
