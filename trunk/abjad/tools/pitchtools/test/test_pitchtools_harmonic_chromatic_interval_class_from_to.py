from abjad import *


def test_pitchtools_harmonic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(-3), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(-2), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(-1), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(0), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(9), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(10), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(11), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-3))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-2))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-1))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(0))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(9))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(10))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(11))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_08( ):
   '''Works with quartertones.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-2.5))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
