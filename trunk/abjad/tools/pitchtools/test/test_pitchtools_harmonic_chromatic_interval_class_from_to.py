from abjad import *


def test_pitchtools_harmonic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(-3), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(-2), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(-1), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(0), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(9), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(10), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(11), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-3))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-2))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-1))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(0))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_harmonic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(9))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(10))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.harmonic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(11))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)
