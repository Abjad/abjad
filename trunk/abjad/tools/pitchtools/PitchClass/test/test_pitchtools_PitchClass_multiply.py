from abjad import *


def test_pitchtools_PitchClass_multiply_01( ):

   assert pitchtools.PitchClass(0).multiply(5) == pitchtools.PitchClass(0)
   assert pitchtools.PitchClass(1).multiply(5) == pitchtools.PitchClass(5)
   assert pitchtools.PitchClass(2).multiply(5) == pitchtools.PitchClass(10)
   assert pitchtools.PitchClass(3).multiply(5) == pitchtools.PitchClass(3)
   assert pitchtools.PitchClass(4).multiply(5) == pitchtools.PitchClass(8)
   assert pitchtools.PitchClass(5).multiply(5) == pitchtools.PitchClass(1)
   assert pitchtools.PitchClass(6).multiply(5) == pitchtools.PitchClass(6)
   assert pitchtools.PitchClass(7).multiply(5) == pitchtools.PitchClass(11)
   assert pitchtools.PitchClass(8).multiply(5) == pitchtools.PitchClass(4)
   assert pitchtools.PitchClass(9).multiply(5) == pitchtools.PitchClass(9)
   assert pitchtools.PitchClass(10).multiply(5) == pitchtools.PitchClass(2)
   assert pitchtools.PitchClass(11).multiply(5) == pitchtools.PitchClass(7)
   
