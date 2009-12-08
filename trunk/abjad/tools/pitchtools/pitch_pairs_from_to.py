from abjad.tools import listtools
from abjad.tools.pitchtools.get_pitches import get_pitches


def pitch_pairs_from_to(expr_1, expr_2):
   '''.. versionadded:: 1.1.2

   Yield ordered pitch pairs from `expr_1` to `expr_2`. ::

      abjad> chord_1 = Chord([0, 1, 2], (1, 4))
      abjad> chord_2 = Chord([3, 4], (1, 4))
      abjad> for pair in pitchtools.pitch_pairs_from_to(chord_1, chord_2):
      ...      pair
      (Pitch(c, 4), Pitch(ef, 4))
      (Pitch(c, 4), Pitch(e, 4))
      (Pitch(cs, 4), Pitch(ef, 4))
      (Pitch(cs, 4), Pitch(e, 4))
      (Pitch(d, 4), Pitch(ef, 4))
      (Pitch(d, 4), Pitch(e, 4))
   '''

   pitches_1 = sorted(get_pitches(expr_1))
   pitches_2 = sorted(get_pitches(expr_2))
   for pair in listtools.pairs_from_to(pitches_1, pitches_2):
      yield pair
