from abjad import *


def test_pitchtools_melodic_counterpoint_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_02( ):
   '''Ascending octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(8)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(2)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_04( ):
   '''Unison.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(1)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_06( ):
   '''Descending octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-8)


def test_pitchtools_melodic_counterpoint_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-3)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)

   mcpi = pitchtools.melodic_counterpoint_interval_class_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert mcpi == pitchtools.MelodicCounterpointIntervalClass(-2)
