from abjad import *


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(-3), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(-2), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(-1), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_02( ):
   '''Ascending octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(0), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(8)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(9), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(10), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(11), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_04( ):
   '''Unison.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(1)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(-3))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(-2))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(-1))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_06( ):
   '''Descending octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(0))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-8)


def test_pitchtools_harmonic_counterpoint_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(9))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(10))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      NamedPitch(12), NamedPitch(11))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)
