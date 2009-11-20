def diatonic_scale_degree_to_letter(diatonic_scale_degree):
   '''Return length-one pitch class letter string corresponding
   to `diatonic_scale_degree`. ::

      abjad> pitchtools.diatonic_scale_degree_to_letter(1)
      'c'
      abjad> pitchtools.diatonic_scale_degree_to_letter(2)
      'd'
      abjad> pitchtools.diatonic_scale_degree_to_letter(3)
      'e'
      abjad> pitchtools.diatonic_scale_degree_to_letter(4)
      'f'
      abjad> pitchtools.diatonic_scale_degree_to_letter(5)
      'g'
      abjad> pitchtools.diatonic_scale_degree_to_letter(6)
      'a'
      abjad> pitchtools.diatonic_scale_degree_to_letter(7)
      'b'
   '''

   return _diatonicScaleDegreeToLetter[diatonic_scale_degree]


_diatonicScaleDegreeToLetter = {
   1: 'c',  2: 'd',  3: 'e',  4: 'f',  5: 'g',  6: 'a',  7: 'b' }
