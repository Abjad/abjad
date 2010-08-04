from abjad import *


def test_pitchtools_harmonic_diatonic_interval_class_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(-3), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(-2), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(-1), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_02( ):
   '''Ascending octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(0), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(9), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(10), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(11), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_04( ):
   '''Unison.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(12))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 1)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-3))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-2))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(-1))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_06( ):
   '''Descending octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(0))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('perfect', 8)


def test_pitchtools_harmonic_diatonic_interval_class_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(9))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 3)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(10))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('major', 2)

   hdic = pitchtools.harmonic_diatonic_interval_class_from_to(
      NamedPitch(12), NamedPitch(11))
   assert hdic == pitchtools.HarmonicDiatonicIntervalClass('minor', 2)
