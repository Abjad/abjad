from abjad.tools.pitchtools.get_pitch_classes import get_pitch_classes
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet


def has_duplicate_pitch_class(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` contains one or more duplicate pitch classes.
   Otherwise false. ::

      abjad> chord = Chord([1, 13, 14], (1, 4))
      abjad> pitchtools.has_duplicate_pitch_class(chord)
      True

   ::

      abjad> chord = Chord([1, 14, 15], (1, 4))
      abjad> pitchtools.has_duplicate_pitch_class(chord)
      False 
   '''
 
   pitch_classes = get_pitch_classes(expr)
   pitch_class_set = PitchClassSet(expr)
   return not len(pitch_classes) == len(pitch_class_set) 
