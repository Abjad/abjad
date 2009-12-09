from abjad import *


def test_pitchtools_melodic_diatonic_interval_from_to_01( ):

   pitch = Pitch(12)

   interval = pitchtools.melodic_diatonic_interval_from_to(pitch, Pitch(12))
   assert interval == pitchtools.MelodicDiatonicInterval('perfect', 1)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('b', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('minor', -2)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('bf', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('major', -2)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('as', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('diminished', -3)


def test_pitchtools_melodic_diatonic_interval_from_to_02( ):

   pitch = Pitch(12)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('a', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('minor', -3)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('af', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('major', -3)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('gs', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('diminished', -4)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      Pitch(12), Pitch('g', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('perfect', -4)
