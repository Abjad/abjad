from abjad.tools.pitchtools.list_numeric_pitch_classes_in_expr import list_numeric_pitch_classes_in_expr
from abjad.tools.pitchtools.NumericPitchClassSet import NumericPitchClassSet


def expr_has_duplicate_numeric_pitch_class(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` contains one or more duplicate pitch classes.
   Otherwise false. ::

      abjad> chord = Chord([1, 13, 14], (1, 4))
      abjad> pitchtools.expr_has_duplicate_named_pitch_class(chord)
      True

   ::

      abjad> chord = Chord([1, 14, 15], (1, 4))
      abjad> pitchtools.expr_has_duplicate_named_pitch_class(chord)
      False 

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.has_duplicate_pitch_class( )`` to
      ``pitchtools.expr_has_duplicate_numeric_pitch_class( )``.
   '''
 
   pitch_classes = list_numeric_pitch_classes_in_expr(expr)
   pitch_class_set = NumericPitchClassSet(expr)
   return not len(pitch_classes) == len(pitch_class_set) 
