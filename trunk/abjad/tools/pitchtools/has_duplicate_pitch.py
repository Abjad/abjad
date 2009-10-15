from abjad.tools.pitchtools.get_pitches import get_pitches
from abjad.tools.pitchtools.PitchSet import PitchSet


def has_duplicate_pitch(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` contains one or more duplicate pitches.
   Otherwise false. ::

      abjad> chord = Chord([13, 13, 14], (1, 4))
      abjad> pitchtools.has_duplicate_pitch(chord)
      True

   ::

      abjad> chord = Chord([13, 14, 15], (1, 4))
      abjad> pitchtools.has_duplicate_pitch(chord)
      False
   '''

   pitches = get_pitches(expr)
   pitch_set = PitchSet(expr)
   return not len(pitches) == len(pitch_set)
