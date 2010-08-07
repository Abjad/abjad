from abjad import *


def test_PitchClass_invert_01( ):
   
   assert pitchtools.NumericPitchClass(0).invert( ) == pitchtools.NumericPitchClass(0)
   assert pitchtools.NumericPitchClass(1).invert( ) == pitchtools.NumericPitchClass(11)
   assert pitchtools.NumericPitchClass(2).invert( ) == pitchtools.NumericPitchClass(10)
   assert pitchtools.NumericPitchClass(3).invert( ) == pitchtools.NumericPitchClass(9)
   assert pitchtools.NumericPitchClass(4).invert( ) == pitchtools.NumericPitchClass(8)
   assert pitchtools.NumericPitchClass(5).invert( ) == pitchtools.NumericPitchClass(7)
   assert pitchtools.NumericPitchClass(6).invert( ) == pitchtools.NumericPitchClass(6)
   assert pitchtools.NumericPitchClass(7).invert( ) == pitchtools.NumericPitchClass(5)
   assert pitchtools.NumericPitchClass(8).invert( ) == pitchtools.NumericPitchClass(4)
   assert pitchtools.NumericPitchClass(9).invert( ) == pitchtools.NumericPitchClass(3)
   assert pitchtools.NumericPitchClass(10).invert( ) == pitchtools.NumericPitchClass(2)
   assert pitchtools.NumericPitchClass(11).invert( ) == pitchtools.NumericPitchClass(1)
