from abjad import *


def test_pitchtools_harmonic_diatonic_interval_from_to_01( ):

   pitch = Pitch(12)

   interval = pitchtools.harmonic_diatonic_interval_from_to(pitch, Pitch(12))
   assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 1)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      pitch, Pitch('b', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('minor', 2)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      pitch, Pitch('bf', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('major', 2)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      Pitch(12), Pitch('as', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 3)


def test_pitchtools_harmonic_diatonic_interval_from_to_02( ):

   pitch = Pitch(12)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      Pitch(12), Pitch('a', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('minor', 3)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      Pitch(12), Pitch('af', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('major', 3)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      Pitch(12), Pitch('gs', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 4)

   interval = pitchtools.harmonic_diatonic_interval_from_to(
      Pitch(12), Pitch('g', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 4)
