from abjad import *


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_01( ):
   '''Ascending intervals greater than an octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(10)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_02( ):
   '''Ascending octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(8)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_03( ):
   '''Ascending intervals less than an octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(3)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_04( ):
   '''Unison.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(1)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_05( ):
   '''Descending intervals greater than an octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(10)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_06( ):
   '''Descending octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(8)


def test_pitchtools_calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch_07( ):
   '''Descending intervals less than an octave.'''

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(3)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)

   hcpi = pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)
