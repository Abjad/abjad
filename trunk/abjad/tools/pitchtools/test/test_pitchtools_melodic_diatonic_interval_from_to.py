from abjad import *


def test_pitchtools_melodic_diatonic_interval_from_to_01( ):

   pitch = NamedPitch(12)

   interval = pitchtools.melodic_diatonic_interval_from_to(pitch, NamedPitch(12))
   assert interval == pitchtools.MelodicDiatonicInterval('perfect', 1)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      pitch, NamedPitch('b', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('minor', -2)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      pitch, NamedPitch('bf', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('major', -2)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      NamedPitch(12), NamedPitch('as', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('diminished', -3)


def test_pitchtools_melodic_diatonic_interval_from_to_02( ):

   pitch = NamedPitch(12)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      NamedPitch(12), NamedPitch('a', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('minor', -3)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      NamedPitch(12), NamedPitch('af', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('major', -3)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      NamedPitch(12), NamedPitch('gs', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('diminished', -4)

   interval = pitchtools.melodic_diatonic_interval_from_to(
      NamedPitch(12), NamedPitch('g', 4))
   assert interval == pitchtools.MelodicDiatonicInterval('perfect', -4)
