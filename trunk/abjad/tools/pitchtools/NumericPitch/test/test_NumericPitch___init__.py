from abjad import *


def test_NumericPitch___init___01( ):
   '''Init with number.'''

   assert pitchtools.NumericPitch(0).number == 0
   assert pitchtools.NumericPitch(0.5).number == 0.5
   assert pitchtools.NumericPitch(12).number == 12
   assert pitchtools.NumericPitch(12.5).number == 12.5
   assert pitchtools.NumericPitch(-12).number == -12
   assert pitchtools.NumericPitch(-12.5).number == -12.5


def test_NumericPitch___init___02( ):
   '''Init with other numeric pitch instance.'''

   assert pitchtools.NumericPitch(pitchtools.NumericPitch(12)).number == 12
