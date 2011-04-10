from abjad.tools.pitchtools.diatonic_pitch_name_to_chromatic_pitch_number import diatonic_pitch_name_to_chromatic_pitch_number


def diatonic_pitch_name_to_chromatic_pitch_class_number(diatonic_pitch_name):
   '''.. versionadded:: 1.1.2

   Convert `diatonic_pitch_name` to chromatic pitch-class number::

      abjad> pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("c''")
      0

   Return integer.
   '''

   chromatic_pitch_number = diatonic_pitch_name_to_chromatic_pitch_number(diatonic_pitch_name)

   return chromatic_pitch_number % 12
