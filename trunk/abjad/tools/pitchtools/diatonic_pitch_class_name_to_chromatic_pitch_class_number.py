def diatonic_pitch_class_name_to_chromatic_pitch_class_number(diatonic_pitch_class_name):
   '''.. versionadded:: 1.1.1

   Convert `diatonic_pitch_class_name` to chromatic pitch-class number::

      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('f')
      5

   Return integer.
   '''
   from abjad.tools import pitchtools

   return _diatonic_pitch_class_name_to_chromatic_pitch_number[diatonic_pitch_class_name]


_diatonic_pitch_class_name_to_chromatic_pitch_number = {
   'c': 0,  'd': 2,  'e': 4,  'f': 5,  'g': 7,  'a': 9,  'b': 11 }
