def one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(diatonic_scale_degree):
   '''Return length-one pitch class letter string corresponding
   to `diatonic_scale_degree`. ::

      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(1)
      'c'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(2)
      'd'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(3)
      'e'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(4)
      'f'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(5)
      'g'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(6)
      'a'
      abjad> pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(7)
      'b'

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.diatonic_scale_degree_to_letter( )`` to
      ``pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.one_indexed_diatonic_scale_degree_number_to_pitch_class_name( )`` to
      ``pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name( )``.
   '''

   diatonic_scale_degree_class = diatonic_scale_degree % 7
   if diatonic_scale_degree_class == 0:
      diatonic_scale_degree_class = 7

   return _diatonic_scale_degree_class_to_letter[
      diatonic_scale_degree_class]

_diatonic_scale_degree_class_to_letter = {
   1: 'c',  2: 'd',  3: 'e',  4: 'f',  5: 'g',  6: 'a',  7: 'b' }
