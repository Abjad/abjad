from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface


class HarmonicInterface(_Interface, _FormatContributor):
   r'''Interface to LilyPond \flageolet command.'''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      #self._natural = None

#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _right(self):
#      '''Format contribution right of leaf.'''
#      result = [ ]
#      if self.natural:
#         result.append(r'\flageolet')
#      return result
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @apply
#   def natural( ):
#      '''Set True to add natural harmonic to leaf.'''
#      def fget(self):
#         return self._natural
#      def fset(self, arg):
#         assert isinstance(arg, (bool, type(None)))
#         self._natural = arg
#      return property(**locals( ))
