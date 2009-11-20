def letter_to_diatonic_scale_degree(letter):
   '''Return positive diatonic scale degree integer corresponding to 
   length-one pitch `letter` string. ::

      abjad> pitchtools.letter_to_diatonic_scale_degree('c')
      1
      abjad> pitchtools.letter_to_diatonic_scale_degree('d')
      2
      abjad> pitchtools.letter_to_diatonic_scale_degree('e')
      3
      abjad> pitchtools.letter_to_diatonic_scale_degree('f')
      4
      abjad> pitchtools.letter_to_diatonic_scale_degree('g')
      5
      abjad> pitchtools.letter_to_diatonic_scale_degree('a')
      6
      abjad> pitchtools.letter_to_diatonic_scale_degree('b')
      7
   '''

   return _letterToDiatonicScaleDegree[letter]


_letterToDiatonicScaleDegree = {
   'c': 1,  'd': 2,  'e': 3,  'f': 4,  'g': 5,  'a': 6,  'b': 7 }
