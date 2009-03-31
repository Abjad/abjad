from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _HarmonicInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self.natural = False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _right(self):
      result = [ ]
      if self.natural:
         result.append(r'\flageolet')
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def natural( ):
      def fget(self):
         return self._natural
      def fset(self, arg):
         assert isinstance(arg, bool)
         self._natural = arg
      return property(**locals( ))
