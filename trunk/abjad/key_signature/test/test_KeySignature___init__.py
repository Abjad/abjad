from abjad import *


def test_KeySignature___init___01( ):
   '''Initialize with pitch class letter string and mode string.
   '''

   ks = KeySignature('g', 'major')
   
   assert ks.pitch_class_letter == 'g'
   assert ks.mode == 'major'
