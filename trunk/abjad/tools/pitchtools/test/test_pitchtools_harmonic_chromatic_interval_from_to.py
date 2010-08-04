from abjad import *


def test_pitchtools_harmonic_chromatic_interval_from_to_01( ):
   '''Ascending intervals greater than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(15)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(14)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_harmonic_chromatic_interval_from_to_02( ):
   '''Ascending octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_harmonic_chromatic_interval_from_to_03( ):
   '''Ascending intervals less than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(3)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(2)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_harmonic_chromatic_interval_from_to_04( ):
   '''Unison.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
   assert hci == pitchtools.HarmonicChromaticInterval(0)


def test_pitchtools_harmonic_chromatic_interval_from_to_05( ):
   '''Descending intervals greater than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
   assert hci == pitchtools.HarmonicChromaticInterval(15)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
   assert hci == pitchtools.HarmonicChromaticInterval(14)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
   assert hci == pitchtools.HarmonicChromaticInterval(13)


def test_pitchtools_harmonic_chromatic_interval_from_to_06( ):
   '''Descending octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
   assert hci == pitchtools.HarmonicChromaticInterval(12)


def test_pitchtools_harmonic_chromatic_interval_from_to_07( ):
   '''Descending intervals less than an octave.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
   assert hci == pitchtools.HarmonicChromaticInterval(3)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
   assert hci == pitchtools.HarmonicChromaticInterval(2)

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
   assert hci == pitchtools.HarmonicChromaticInterval(1)


def test_pitchtools_harmonic_chromatic_interval_from_to_08( ):
   '''Works with quartertones.'''

   hci = pitchtools.harmonic_chromatic_interval_from_to(
      pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2.5))
   assert hci == pitchtools.HarmonicChromaticInterval(14.5)
