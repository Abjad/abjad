from abjad.tools.pitchtools.list_numbered_chromatic_pitch_classes_in_expr import list_numbered_chromatic_pitch_classes_in_expr
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet


def expr_has_duplicate_numbered_chromatic_pitch_class(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` duplicated numeric chromatic pitch-class.
   Otherwise false::

      abjad> chord = Chord([1, 13, 14], (1, 4))
      abjad> pitchtools.expr_has_duplicate_named_chromatic_pitch_class(chord)
      True

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.expr_has_duplicate_numeric_chromatic_pitch_class( )`` to
      ``pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class( )``.
   '''
 
   pitch_classes = list_numbered_chromatic_pitch_classes_in_expr(expr)
   pitch_class_set = NumberedChromaticPitchClassSet(expr)
   return not len(pitch_classes) == len(pitch_class_set) 
