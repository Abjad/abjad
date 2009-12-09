from abjad import *


def test_pitchtools_melodic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-3), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-2), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-1), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(0), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(9), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(10), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(11), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(12))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(0)


def test_pitchtools_melodic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-3))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-2))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-1))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(0))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(9))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-3)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(10))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(11))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_08( ):
   '''Quartertones.'''

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-2.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)

   mcic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(9.5))
   assert mcic == pitchtools.MelodicChromaticIntervalClass(-2.5)
