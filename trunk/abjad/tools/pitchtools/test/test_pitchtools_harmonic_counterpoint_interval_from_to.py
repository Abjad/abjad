from abjad import *


def test_pitchtools_harmonic_counterpoint_interval_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(-3), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(10)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(-2), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(-1), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)


def test_pitchtools_harmonic_counterpoint_interval_from_to_02( ):
   '''Ascending octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(0), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(8)


def test_pitchtools_harmonic_counterpoint_interval_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(9), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(3)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(10), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(11), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)


def test_pitchtools_harmonic_counterpoint_interval_from_to_04( ):
   '''Unison.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(12))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(1)


def test_pitchtools_harmonic_counterpoint_interval_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(-3))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(10)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(-2))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(-1))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(9)


def test_pitchtools_harmonic_counterpoint_interval_from_to_06( ):
   '''Descending octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(0))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(8)


def test_pitchtools_harmonic_counterpoint_interval_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(9))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(3)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(10))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)

   hcpi = pitchtools.harmonic_counterpoint_interval_from_to(
      NamedPitch(12), NamedPitch(11))
   assert hcpi == pitchtools.HarmonicCounterpointInterval(2)
