from abjad import *


def test_pitchtools_PitchClass_invert_01( ):
   
   assert pitchtools.PitchClass(0).invert( ) == pitchtools.PitchClass(0)
   assert pitchtools.PitchClass(1).invert( ) == pitchtools.PitchClass(11)
   assert pitchtools.PitchClass(2).invert( ) == pitchtools.PitchClass(10)
   assert pitchtools.PitchClass(3).invert( ) == pitchtools.PitchClass(9)
   assert pitchtools.PitchClass(4).invert( ) == pitchtools.PitchClass(8)
   assert pitchtools.PitchClass(5).invert( ) == pitchtools.PitchClass(7)
   assert pitchtools.PitchClass(6).invert( ) == pitchtools.PitchClass(6)
   assert pitchtools.PitchClass(7).invert( ) == pitchtools.PitchClass(5)
   assert pitchtools.PitchClass(8).invert( ) == pitchtools.PitchClass(4)
   assert pitchtools.PitchClass(9).invert( ) == pitchtools.PitchClass(3)
   assert pitchtools.PitchClass(10).invert( ) == pitchtools.PitchClass(2)
   assert pitchtools.PitchClass(11).invert( ) == pitchtools.PitchClass(1)
