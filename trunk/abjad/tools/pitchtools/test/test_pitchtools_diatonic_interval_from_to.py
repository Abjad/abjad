from abjad import *


def test_pitchtools_diatonic_interval_from_to_01( ):

   pitch = Pitch(12)

   interval = pitchtools.diatonic_interval_from_to(pitch, Pitch(12))
   assert interval == pitchtools.DiatonicInterval('perfect', 1)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('b', 4))
   assert interval == pitchtools.DiatonicInterval('minor', -2)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('bf', 4))
   assert interval == pitchtools.DiatonicInterval('major', -2)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('as', 4))
   assert interval == pitchtools.DiatonicInterval('diminished', -3)


def test_pitchtools_diatonic_interval_from_to_02( ):

   pitch = Pitch(12)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('a', 4))
   assert interval == pitchtools.DiatonicInterval('minor', -3)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('af', 4))
   assert interval == pitchtools.DiatonicInterval('major', -3)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('gs', 4))
   assert interval == pitchtools.DiatonicInterval('diminished', -4)

   interval = pitchtools.diatonic_interval_from_to(Pitch(12), Pitch('g', 4))
   assert interval == pitchtools.DiatonicInterval('perfect', -4)
