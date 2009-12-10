from abjad import *


def test_pitchtools_harmonic_chromatic_interval_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(-3), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(15)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(-2), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(14)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(-1), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_harmonic_chromatic_interval_from_to_02( ):
   '''Ascending octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(0), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_harmonic_chromatic_interval_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(9), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(3)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(10), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(2)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(11), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_harmonic_chromatic_interval_from_to_04( ):
   '''Unison.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(0)


def test_pitchtools_harmonic_chromatic_interval_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(-3))
   assert hci == pitchtools.HarmonicChromaticInterval(15)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(-2))
   assert hci == pitchtools.HarmonicChromaticInterval(14)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(-1))
   assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_harmonic_chromatic_interval_from_to_06( ):
   '''Descending octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(0))
   assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_harmonic_chromatic_interval_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(9))
   assert hci == pitchtools.HarmonicChromaticInterval(3)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(10))
   assert hci == pitchtools.HarmonicChromaticInterval(2)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(11))
   assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_harmonic_chromatic_interval_from_to_08( ):
   '''Works with quartertones.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      Pitch(12), Pitch(-2.5))
   assert hci == pitchtools.HarmonicChromaticInterval(14.5)
