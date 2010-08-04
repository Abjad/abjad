from abjad import *


def test_NamedPitch___sub___01( ):

   pitch = NamedPitch(12)
   diatonic_interval = pitchtools.MelodicDiatonicInterval('diminished', 3)

   assert pitch - diatonic_interval == NamedPitch('as', 4)


def test_NamedPitch___sub___02( ):

   pitch = NamedPitch(12)
   chromatic_interval = pitchtools.MelodicChromaticInterval(2)

   assert pitch - chromatic_interval == NamedPitch('bf', 4)


def test_NamedPitch___sub___03( ):

   pitch_1 = NamedPitch(12)
   pitch_2 = NamedPitch(10)

   assert pitch_1 - pitch_2 == pitchtools.MelodicDiatonicInterval('major', -2)
   assert pitch_2 - pitch_1 == pitchtools.MelodicDiatonicInterval('major', 2) 
