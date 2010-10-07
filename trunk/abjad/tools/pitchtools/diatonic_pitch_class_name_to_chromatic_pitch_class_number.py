def diatonic_pitch_class_name_to_chromatic_pitch_class_number(diatonic_pitch_class_name):
   '''Return nonnegative pitch class integer corresponding to 
   length-one pitch class `letter` string. ::

      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('c')
      0
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('d')
      2
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('e')
      4
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('f')
      5
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('g')
      7
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('a')
      9
      abjad> pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number('b')
      11
   '''
   from abjad.tools import pitchtools

   return _diatonic_pitch_class_name_to_chromatic_pitch_number[diatonic_pitch_class_name]


_diatonic_pitch_class_name_to_chromatic_pitch_number = {
   'c': 0,  'd': 2,  'e': 4,  'f': 5,  'g': 7,  'a': 9,  'b': 11 }
