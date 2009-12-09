from abjad import *


def test_pitchtools_melodic_chromatic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-3), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(3)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-2), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(2)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(-1), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(0), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(9), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(3)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(10), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(2)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(11), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_04( ):
   '''Unison.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(12))
   assert cic == pitchtools.MelodicChromaticIntervalClass(0)


def test_pitchtools_melodic_chromatic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-3))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-3)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-2))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-2)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(-1))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-1)


def test_pitchtools_melodic_chromatic_interval_class_from_to_06( ):
   '''Descending octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(0))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-12)


def test_pitchtools_melodic_chromatic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(9))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-3)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(10))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-2)

   cic = pitchtools.melodic_chromatic_interval_class_from_to(
      Pitch(12), Pitch(11))
   assert cic == pitchtools.MelodicChromaticIntervalClass(-1)
