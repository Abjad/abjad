from abjad.tools import listtools
from abjad.tools.pitchtools.list_named_pitches_in_expr import list_named_pitches_in_expr


def list_unordered_named_chromatic_pitch_pairs_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Yield unordered pitch pairs in `expr`. ::

      abjad> for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(Chord([0, 1, 2, 3], (1, 4))):
      ...     pair
      ... 
      (NamedPitch(c, 4), NamedPitch(cs, 4))
      (NamedPitch(c, 4), NamedPitch(d, 4))
      (NamedPitch(c, 4), NamedPitch(ef, 4))
      (NamedPitch(d, 4), NamedPitch(cs, 4))
      (NamedPitch(cs, 4), NamedPitch(ef, 4))
      (NamedPitch(d, 4), NamedPitch(ef, 4))

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_pairs_within( )`` to
      ``pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.list_unordered_pitch_pairs_in_expr( )`` to
      ``pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr( )``.
   '''

   for pair in listtools.get_unordered_pairs(sorted(list_named_pitches_in_expr(expr))):
      yield pair
