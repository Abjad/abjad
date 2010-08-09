from abjad import *


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_01( ):
   '''Ascending intervals greater than an octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(10)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(9)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(9)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_02( ):
   '''Ascending octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(8)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_03( ):
   '''Ascending intervals less than an octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(3)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(2)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(2)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_04( ):
   '''Unison.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert mcpi == pitchtools.MelodicCounterpointInterval(1)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_05( ):
   '''Descending intervals greater than an octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-10)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-9)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-9)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_06( ):
   '''Descending octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-8)


def test_pitchtools_calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch_07( ):
   '''Descending intervals less than an octave.'''

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-3)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-2)

   mcpi = pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert mcpi == pitchtools.MelodicCounterpointInterval(-2)
