from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface


class _HarmonicInterface(_Interface, _FormatContributor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self.natural = False

   ## PUBLIC ATTRIBUTES ##

   @apply
   def natural( ):
      def fget(self):
         return self._natural
      def fset(self, arg):
         assert isinstance(arg, bool)
         self._natural = arg
      return property(**locals( ))

   @property
   def right(self):
      result = [ ]
      if self.natural:
         result.append(r'\flageolet')
      return result

