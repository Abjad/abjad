from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.tools.markuptools import Markup


class MarkupInterface(_Interface, _FormatContributor):
   '''Manage LilyPond markup.
   Handles no LilyPond grob.
   '''

   def __init__(self, client):
      '''Bind to client and set up and down to empty lists.'''
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._down = [ ]
      self._up = [ ]

   ## PRIVATE ATTRIBUTES ##

   @property
   def _right(self):
      '''Format contribution to right of leaf.'''
      result = [ ]
      if len(self.up):
         string = '^ %s' % self._direction_to_format_string('up')
         result.append(string)
      if len(self.down):
         string = '_ %s' % self._direction_to_format_string('down')
         result.append(string)
      return result

   ## PRIVATE METHODS ##

   def _direction_to_format_string(self, direction):
      result = [ ]
      for x in getattr(self, direction):
         if isinstance(x, Markup):
            result.append(x.contents)
         else:
            result.append(str(x))
      if len(result) == 1:
         return r'\markup { %s }' % result[0]
      elif 1 < len(result):
         return r'\markup { \column { %s } }' % ' '.join(result)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def down( ):
      '''List of markup to position below staff.'''
      def fget(self):
         return self._down
      def fset(self, arg):
         if arg is None or arg == [ ]:
            self._down = [ ]
         elif isinstance(arg, list):
            self._down = arg
         else:
            self._down = [arg]
            #raise ValueError('set leaf markup with append( ) and extend( ).')
      return property(**locals( ))

   @apply
   def up( ):
      '''List of markup to position above staff.'''
      def fget(self):
         return self._up
      def fset(self, arg):
         if arg is None or arg == [ ]:
            self._up = [ ]
         elif isinstance(arg, list):
            self._up = arg
         else:
            self._up = [arg]
            #raise ValueError('set leaf markup with append( ) and extend( ).')
      return property(**locals( ))
