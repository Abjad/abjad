from abjad import *


def test_pitchtools_calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch_01( ):

   pitch = pitchtools.NamedPitch(12)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(pitch, pitchtools.NamedPitch(12))
   assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 1)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitch, pitchtools.NamedPitch('b', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('minor', 2)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitch, pitchtools.NamedPitch('bf', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('major', 2)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch('as', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 3)


def test_pitchtools_calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch_02( ):

   pitch = pitchtools.NamedPitch(12)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch('a', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('minor', 3)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch('af', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('major', 3)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch('gs', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('diminished', 4)

   interval = pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch('g', 4))
   assert interval == pitchtools.HarmonicDiatonicInterval('perfect', 4)
