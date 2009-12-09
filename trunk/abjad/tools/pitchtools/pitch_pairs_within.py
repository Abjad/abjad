from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def pitch_pairs_within(expr):
   '''.. versionadded:: 1.1.2

   Yield unordered pitch pairs in `expr`. ::

      abjad> for pair in pitchtools.pitch_pairs_within(Chord([0, 1, 2, 3], (1, 4))):
      ...     pair
      ... 
      (Pitch(c, 4), Pitch(cs, 4))
      (Pitch(c, 4), Pitch(d, 4))
      (Pitch(c, 4), Pitch(ef, 4))
      (Pitch(d, 4), Pitch(cs, 4))
      (Pitch(cs, 4), Pitch(ef, 4))
      (Pitch(d, 4), Pitch(ef, 4))
   '''

   for pair in listtools.get_unordered_pairs(sorted(get_pitches(expr))):
      yield pair
