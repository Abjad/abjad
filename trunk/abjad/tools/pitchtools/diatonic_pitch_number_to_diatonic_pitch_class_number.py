from abjad.tools.pitchtools.is_diatonic_pitch_number import is_diatonic_pitch_number


def diatonic_pitch_number_to_diatonic_pitch_class_number(diatonic_pitch_number):
   '''.. versionadded:: 1.1.2

   Convert `diatonic_pitch_number` to diatonic pitch-class number::

      abjad> pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(7)
      0
   '''

   if not is_diatonic_pitch_number(diatonic_pitch_number):
      raise TypeError

   return diatonic_pitch_number % 7
