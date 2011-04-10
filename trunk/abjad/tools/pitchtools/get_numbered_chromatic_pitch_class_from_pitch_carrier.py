from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass


def get_numbered_chromatic_pitch_class_from_pitch_carrier(pitch_carrier):
   '''.. versionadded:: 1.1.2

   Get numeric chromatic pitch-class from `pitch_carrier`::

      abjad> note = Note("cs'4")
      abjad> pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(note)
      NumberedChromaticPitchClass(1)

   Raise missing pitch error on empty chords.

   Raise extra pitch error on many-note chords.

   Return numbered chromatic pitch-class.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier( )`` to
      ``pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier( )``.
   '''

   pitch = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier)
   pitch_class = NumberedChromaticPitchClass(pitch)
   return pitch_class
