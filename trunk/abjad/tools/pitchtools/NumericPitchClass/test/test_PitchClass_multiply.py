from abjad import *


def test_PitchClass_multiply_01( ):

   assert pitchtools.NumericPitchClass(0).multiply(5) == pitchtools.NumericPitchClass(0)
   assert pitchtools.NumericPitchClass(1).multiply(5) == pitchtools.NumericPitchClass(5)
   assert pitchtools.NumericPitchClass(2).multiply(5) == pitchtools.NumericPitchClass(10)
   assert pitchtools.NumericPitchClass(3).multiply(5) == pitchtools.NumericPitchClass(3)
   assert pitchtools.NumericPitchClass(4).multiply(5) == pitchtools.NumericPitchClass(8)
   assert pitchtools.NumericPitchClass(5).multiply(5) == pitchtools.NumericPitchClass(1)
   assert pitchtools.NumericPitchClass(6).multiply(5) == pitchtools.NumericPitchClass(6)
   assert pitchtools.NumericPitchClass(7).multiply(5) == pitchtools.NumericPitchClass(11)
   assert pitchtools.NumericPitchClass(8).multiply(5) == pitchtools.NumericPitchClass(4)
   assert pitchtools.NumericPitchClass(9).multiply(5) == pitchtools.NumericPitchClass(9)
   assert pitchtools.NumericPitchClass(10).multiply(5) == pitchtools.NumericPitchClass(2)
   assert pitchtools.NumericPitchClass(11).multiply(5) == pitchtools.NumericPitchClass(7)
   
