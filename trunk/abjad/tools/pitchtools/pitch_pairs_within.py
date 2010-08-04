from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def pitch_pairs_within(expr):
   '''.. versionadded:: 1.1.2

   Yield unordered pitch pairs in `expr`. ::

      abjad> for pair in pitchtools.pitch_pairs_within(Chord([0, 1, 2, 3], (1, 4))):
      ...     pair
      ... 
      (NamedPitch(c, 4), NamedPitch(cs, 4))
      (NamedPitch(c, 4), NamedPitch(d, 4))
      (NamedPitch(c, 4), NamedPitch(ef, 4))
      (NamedPitch(d, 4), NamedPitch(cs, 4))
      (NamedPitch(cs, 4), NamedPitch(ef, 4))
      (NamedPitch(d, 4), NamedPitch(ef, 4))
   '''

   for pair in listtools.get_unordered_pairs(sorted(get_pitches(expr))):
      yield pair
