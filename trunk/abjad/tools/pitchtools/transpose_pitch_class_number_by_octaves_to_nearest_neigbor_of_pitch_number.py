def transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(pitch_number, pc):
   '''Return integer pitch number within one tritone
   of `pitch_number` and with pitch class 
   equal to `pc`. ::

      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 0)
      12
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 1)
      13
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 2)
      14
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 3)
      15
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 4)
      16
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 5)
      17
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 6)
      6
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 7)
      7
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 8)
      8
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 9)
      9
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 10)
      10
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 11)
      11
      abjad> pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number(12, 12)
      12

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.nearest_neighbor( )`` to
      ``pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neigbor_of_pitch_number( )``.
   '''
   
   targetPC = pitch_number % 12
   down = (targetPC - pc) % 12
   up = (pc - targetPC) % 12
   if up < down:
      return pitch_number + up
   else:
      return pitch_number - down
