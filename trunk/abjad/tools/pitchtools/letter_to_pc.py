def letter_to_pc(letter):
   '''Return nonnegative pitch class integer corresponding to 
   length-one pitch class `letter` string. ::

      abjad> pitchtools.letter_to_pc('c')
      0
      abjad> pitchtools.letter_to_pc('d')
      2
      abjad> pitchtools.letter_to_pc('e')
      4
      abjad> pitchtools.letter_to_pc('f')
      5
      abjad> pitchtools.letter_to_pc('g')
      7
      abjad> pitchtools.letter_to_pc('a')
      9
      abjad> pitchtools.letter_to_pc('b')
      11
   '''

   return _letterToPC[letter]


_letterToPC = {
   'c': 0,  'd': 2,  'e': 4,  'f': 5,  'g': 7,  'a': 9,  'b': 11 }
