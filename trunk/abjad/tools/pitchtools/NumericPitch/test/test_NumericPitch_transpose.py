from abjad import *


def test_NumericPitch_transpose_01( ):

   assert pitchtools.NumericPitch(12).transpose(6).number == 18
   assert pitchtools.NumericPitch(12).transpose(-6).number == 6
   assert pitchtools.NumericPitch(12).transpose(0).number == 12
   assert pitchtools.NumericPitch(12).transpose(0.5).number == 12.5
