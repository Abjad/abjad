from abjad.tools.pitchtools.is_chromatic_pitch_number import is_chromatic_pitch_number


def chromatic_pitch_number_to_chromatic_pitch_class_number(chromatic_pitch_number):
   '''.. versionadded:: 1.1.2

   Convert `chromatic_pitch_number` to chromatic pitch-class number::

      abjad> pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(13)
      1

   Return integer or float.
   '''

   if not is_chromatic_pitch_number(chromatic_pitch_number):
      raise TypeError

   return chromatic_pitch_number % 12
