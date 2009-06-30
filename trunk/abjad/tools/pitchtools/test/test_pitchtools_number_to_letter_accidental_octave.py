from abjad import *


def test_pitchtools_number_to_letter_accidental_octave_01( ):

   t = pitchtools.number_to_letter_accidental_octave(12, 'mixed')
   assert t == ('c', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(13, 'mixed')
   assert t == ('c', 's', 5)
   t = pitchtools.number_to_letter_accidental_octave(14, 'mixed')
   assert t == ('d', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(15, 'mixed')
   assert t == ('e', 'f', 5)
   t = pitchtools.number_to_letter_accidental_octave(16, 'mixed')
   assert t == ('e', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(17, 'mixed')
   assert t == ('f', '', 5)


def test_pitchtools_number_to_letter_accidental_octave_02( ):

   t = pitchtools.number_to_letter_accidental_octave(12, 'sharps')
   assert t == ('c', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(13, 'sharps')
   assert t == ('c', 's', 5)
   t = pitchtools.number_to_letter_accidental_octave(14, 'sharps')
   assert t == ('d', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(15, 'sharps')
   assert t == ('d', 's', 5)
   t = pitchtools.number_to_letter_accidental_octave(16, 'sharps')
   assert t == ('e', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(17, 'sharps')
   assert t == ('f', '', 5)


def test_pitchtools_number_to_letter_accidental_octave_03( ):

   t = pitchtools.number_to_letter_accidental_octave(12, 'flats')
   assert t == ('c', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(13, 'flats')
   assert t == ('d', 'f', 5)
   t = pitchtools.number_to_letter_accidental_octave(14, 'flats')
   assert t == ('d', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(15, 'flats')
   assert t == ('e', 'f', 5)
   t = pitchtools.number_to_letter_accidental_octave(16, 'flats')
   assert t == ('e', '', 5)
   t = pitchtools.number_to_letter_accidental_octave(17, 'flats')
   assert t == ('f', '', 5)
