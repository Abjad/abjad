from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface


class _MarkupInterface(_Interface, _FormatContributor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._down = [ ]
      self._up = [ ]

   ## PUBLIC ATTRIBUTES ##

   @apply
   def down( ):
      def fget(self):
         return self._down
      def fset(self, arg):
         if arg is None or arg == [ ]:
            self._down = [ ]
         else:
            raise ValueError('set leaf markup with append( ) and extend( ).')
      return property(**locals( ))

   @property
   def right(self):
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

   @apply
   def up( ):
      def fget(self):
         return self._up
      def fset(self, arg):
         if arg is None or arg == [ ]:
            self._up = [ ]
         else:
            raise ValueError('set leaf markup with append( ) and extend( ).')
      return property(**locals( ))
