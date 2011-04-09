def diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number(
   diatonic_pitch_class_name):
   '''.. versionadded:: 1.1.1

   Convert `diatonic_pitch_class_name` to one-indexed diatonic scale degree::

      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('c')
      1

   Return positive integer.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.letter_to_diatonic_scale_degree( )`` to
      ``pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number( )``.
   '''

   return _diatonic_pitch_class_name_to_diatonic_pitch_class_number[diatonic_pitch_class_name]


_diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
   'c': 1,  'd': 2,  'e': 3,  'f': 4,  'g': 5,  'a': 6,  'b': 7 }
