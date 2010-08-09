def pitch_letter_to_pitch_class_number(letter):
   '''Return nonnegative pitch class integer corresponding to 
   length-one pitch class `letter` string. ::

      abjad> pitchtools.pitch_letter_to_pitch_class_number('c')
      0
      abjad> pitchtools.pitch_letter_to_pitch_class_number('d')
      2
      abjad> pitchtools.pitch_letter_to_pitch_class_number('e')
      4
      abjad> pitchtools.pitch_letter_to_pitch_class_number('f')
      5
      abjad> pitchtools.pitch_letter_to_pitch_class_number('g')
      7
      abjad> pitchtools.pitch_letter_to_pitch_class_number('a')
      9
      abjad> pitchtools.pitch_letter_to_pitch_class_number('b')
      11

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.letter_to_pc( )`` to
      ``pitchtools.pitch_letter_to_pitch_class_number( )``.
   '''

   return _letterToPC[letter]


_letterToPC = {
   'c': 0,  'd': 2,  'e': 4,  'f': 5,  'g': 7,  'a': 9,  'b': 11 }
