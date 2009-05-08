from abjad import *


def test_pitchtools_are_in_octave_order_01( ):
   '''True when all pcs appear in octave order in pitches.'''

   pcs = [2, 7, 10]      
   pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
   assert pitchtools.are_in_octave_order(pcs, pitches)


def test_pitchtools_are_in_octave_order_02( ):
   '''True when all pcs appear in octave order in pitches.'''

   pcs = [2, 3, 4]
   pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
   assert not pitchtools.are_in_octave_order(pcs, pitches)
