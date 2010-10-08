from abjad import *


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_01( ):
   '''Ascending intervals greater than an octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_02( ):
   '''Ascending octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_03( ):
   '''Ascending intervals less than an octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_04( ):
   '''Unison.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(0)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_05( ):
   '''Descending intervals greater than an octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_06( ):
   '''Descending octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(12)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_07( ):
   '''Descending intervals less than an octave.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(3)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2)

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(1)


def test_pitchtools_calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier_08( ):
   '''Works with quartertones.'''

   hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
   assert hcic == pitchtools.HarmonicChromaticIntervalClass(2.5)
