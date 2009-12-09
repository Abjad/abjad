from abjad import *


def test_pitchtools_melodic_diatonic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(-3), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 3)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(-2), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', 2)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(-1), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 2)


def test_pitchtools_melodic_diatonic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(0), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_melodic_diatonic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(9), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 3)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(10), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', 2)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(11), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', 2)


def test_pitchtools_melodic_diatonic_interval_class_from_to_04( ):
   '''Unison.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(12))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', 1)


def test_pitchtools_melodic_diatonic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(-3))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -3)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(-2))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', -2)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(-1))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -2)


def test_pitchtools_melodic_diatonic_interval_class_from_to_06( ):
   '''Descending octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(0))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('perfect', -8)


def test_pitchtools_melodic_diatonic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(9))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -3)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(10))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('major', -2)

   mcpi = pitchtools.melodic_diatonic_interval_class_from_to(
      Pitch(12), Pitch(11))
   assert mcpi == pitchtools.MelodicDiatonicIntervalClass('minor', -2)
