from abjad import *


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_01( ):
   '''Ascending intervals greater than an octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_02( ):
   '''Ascending octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(12)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_03( ):
   '''Ascending intervals less than an octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_04( ):
   '''Unison.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(0)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_05( ):
   '''Descending intervals greater than an octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_06( ):
   '''Descending octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_07( ):
   '''Descending intervals less than an octave.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_calculate_melodic_chromatic_interval_class_from_pitch_to_pitch_08( ):
   '''Quartertones.'''

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)

   mcic = pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)
