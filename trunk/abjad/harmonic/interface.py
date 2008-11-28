from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _HarmonicInterface(_Interface, _FormatCarrier):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._set = None

   ### OVERLOADS ###

   ### TODO: figure out if these comparison definitions should go away

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def __nonzero__(self):
      return bool(self._set)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\flageolet')
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      self._set = None
