from abjad import *


def test_Pitch___sub___01( ):

   pitch = Pitch(12)
   diatonic_interval = pitchtools.DiatonicInterval('diminished', 3)

   assert pitch - diatonic_interval == Pitch('as', 4)


def test_Pitch___sub___02( ):

   pitch = Pitch(12)
   chromatic_interval = pitchtools.ChromaticInterval(2)

   assert pitch - chromatic_interval == Pitch('bf', 4)


def test_Pitch___sub___03( ):

   pitch_1 = Pitch(12)
   pitch_2 = Pitch(10)

   assert pitch_1 - pitch_2 == pitchtools.DiatonicInterval('major', -2)
   assert pitch_2 - pitch_1 == pitchtools.DiatonicInterval('major', 2) 
