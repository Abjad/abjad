from abjad import *


def test_pitchtools_melodic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(0)


def test_pitchtools_melodic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_08( ):
   '''Quartertones.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)
