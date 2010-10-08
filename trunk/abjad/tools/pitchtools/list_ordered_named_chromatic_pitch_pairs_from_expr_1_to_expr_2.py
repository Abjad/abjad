from abjad.tools import listtools
from abjad.tools.pitchtools.list_named_pitches_in_expr import list_named_pitches_in_expr


def list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(expr_1, expr_2):
   '''.. versionadded:: 1.1.2

   Yield ordered pitch pairs from `expr_1` to `expr_2`. ::

      abjad> chord_1 = Chord([0, 1, 2], (1, 4))
      abjad> chord_2 = Chord([3, 4], (1, 4))
      abjad> for pair in pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(chord_1, chord_2):
      ...      pair
      (NamedPitch(c, 4), NamedPitch(ef, 4))
      (NamedPitch(c, 4), NamedPitch(e, 4))
      (NamedPitch(cs, 4), NamedPitch(ef, 4))
      (NamedPitch(cs, 4), NamedPitch(e, 4))
      (NamedPitch(d, 4), NamedPitch(ef, 4))
      (NamedPitch(d, 4), NamedPitch(e, 4))

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_pairs_from_to( )`` to
      ``pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.list_ordered_pitch_pairs_from_expr_cross_to_expr( )`` to
      ``pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2( )``.
   '''

   pitches_1 = sorted(list_named_pitches_in_expr(expr_1))
   pitches_2 = sorted(list_named_pitches_in_expr(expr_2))
   for pair in listtools.pairs_from_to(pitches_1, pitches_2):
      yield pair
