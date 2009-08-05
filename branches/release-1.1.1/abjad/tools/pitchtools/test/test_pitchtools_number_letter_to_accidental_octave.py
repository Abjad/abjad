from abjad import *


def test_pitchtools_number_letter_to_accidental_octave_01( ):

   t = pitchtools.number_letter_to_accidental_octave(12, 'b')
   assert t == ('s', 4)
   t = pitchtools.number_letter_to_accidental_octave(12, 'c')
   assert t == ('', 5)
   t = pitchtools.number_letter_to_accidental_octave(12, 'd')
   assert t == ('ff', 5)


def test_pitchtools_number_letter_to_accidental_octave_02( ):

   t = pitchtools.number_letter_to_accidental_octave(13, 'b')
   assert t == ('ss', 4)
   t = pitchtools.number_letter_to_accidental_octave(13, 'c')
   assert t == ('s', 5)
   t = pitchtools.number_letter_to_accidental_octave(13, 'd')
   assert t == ('f', 5)


def test_pitchtools_number_letter_to_accidental_octave_03( ):

   t = pitchtools.number_letter_to_accidental_octave(14, 'c')
   assert t == ('ss', 5)
   t = pitchtools.number_letter_to_accidental_octave(14, 'd')
   assert t == ('', 5)
   t = pitchtools.number_letter_to_accidental_octave(14, 'e')
   assert t == ('ff', 5)
