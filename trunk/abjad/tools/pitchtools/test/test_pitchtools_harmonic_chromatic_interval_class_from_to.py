from abjad import *


def test_pitchtools_harmonic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_08( ):
   '''Works with quartertones.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
