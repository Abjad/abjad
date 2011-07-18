from collections import Iterable
from abjad import Fraction
from abjad.core import _Immutable
from abjad.core import _ImmutableDictionary
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import Offset
from abjad.tools.quantizationtools.QGridSearchTree import QGridSearchTree
from abjad.tools.quantizationtools.is_valid_beatspan import is_valid_beatspan
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds


class QGridTempoLookup(_Immutable, _ImmutableDictionary):
   '''A utility class for matching fractional offsets within a beat
   to their tempo-scaled (real-time) millisecond values.
   '''

   __slots__ = ('_beatspan', '_tempo',)

   def __init__(self, offsets, beatspan, tempo):

      if isinstance(offsets, QGridSearchTree):
         offsets = offsets.offsets
      elif isinstance(offsets, Iterable):
         assert all([isinstance(x, Fraction) and 0 <= x <= 1 for x in offsets])
      else:
         raise ValueError
      assert is_valid_beatspan(beatspan)
      assert isinstance(tempo, TempoMark)

      for offset in offsets:
         dict.__setitem__(self, offset, tempo_scaled_rational_to_milliseconds(offset * beatspan, tempo))
      object.__setattr__(self, '_beatspan', beatspan)
      object.__setattr__(self, '_tempo', tempo)

   def __getnewargs__(self):
      return tuple(self.keys( )), self.beatspan, self.tempo

   ## PUBLIC ATTRIBUTES ##

   @property
   def beatspan(self):
      return self._beatspan

   @property
   def tempo(self):
      return self._tempo
