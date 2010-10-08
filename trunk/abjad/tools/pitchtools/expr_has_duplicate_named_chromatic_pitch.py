from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr
from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet


def expr_has_duplicate_named_chromatic_pitch(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` contains one or more duplicate pitches.
   Otherwise false. ::

      abjad> chord = Chord([13, 13, 14], (1, 4))
      abjad> pitchtools.expr_has_duplicate_named_chromatic_pitch(chord)
      True

   ::

      abjad> chord = Chord([13, 14, 15], (1, 4))
      abjad> pitchtools.expr_has_duplicate_named_chromatic_pitch(chord)
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.has_duplicate_pitch( )`` to
      ``pitchtools.expr_has_duplicate_named_chromatic_pitch( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.expr_has_duplicate_named_chromatic_pitch( )`` to
      ``pitchtools.expr_has_duplicate_named_chromatic_pitch( )``.
   '''

   pitches = list_named_chromatic_pitches_in_expr(expr)
   pitch_set = NamedChromaticPitchSet(pitches)
   return not len(pitches) == len(pitch_set)
