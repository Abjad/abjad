from abjad import *


def test_pitchtools_name_to_letter_accidental_01( ):

   assert pitchtools.name_to_letter_accidental('c') == ('c', '')
   assert pitchtools.name_to_letter_accidental('cs') == ('c', 's')
   assert pitchtools.name_to_letter_accidental('d') == ('d', '')
   assert pitchtools.name_to_letter_accidental('ds') == ('d', 's')

