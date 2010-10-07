def diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number(letter):
   '''Return positive diatonic scale degree integer corresponding to 
   length-one pitch `letter` string. ::

      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('c')
      1
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('d')
      2
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('e')
      3
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('f')
      4
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('g')
      5
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('a')
      6
      abjad> pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number('b')
      7

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.letter_to_diatonic_scale_degree( )`` to
      ``pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number( )`` to
      ``pitchtools.diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number( )``.
   '''

   return _letterToDiatonicScaleDegree[letter]


_letterToDiatonicScaleDegree = {
   'c': 1,  'd': 2,  'e': 3,  'f': 4,  'g': 5,  'a': 6,  'b': 7 }
