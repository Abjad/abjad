from abjad import *


def test_NamedChromaticPitch_diatonic_pitch_number_01( ):
   '''Pitches referentially equal.
   '''

   p1 = pitchtools.NamedChromaticPitch('fs', 4)

   assert     p1.diatonic_pitch_number == p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number != p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p1.diatonic_pitch_number
   assert     p1.diatonic_pitch_number >= p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number <  p1.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p1.diatonic_pitch_number


def test_NamedChromaticPitch_diatonic_pitch_number_02( ):
   '''Pitches by name, accidental and octave.
   '''

   p1, p2 = pitchtools.NamedChromaticPitch('fs', 4), pitchtools.NamedChromaticPitch('fs', 4)

   assert     p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedChromaticPitch_diatonic_pitch_number_03( ):
   '''Pitches enharmonically equal.
   '''

   p1, p2 = pitchtools.NamedChromaticPitch('fs', 4), pitchtools.NamedChromaticPitch('gf', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedChromaticPitch_diatonic_pitch_number_04( ):
   '''Pitches manifestly different.
   '''

   p1, p2 = pitchtools.NamedChromaticPitch('f', 4), pitchtools.NamedChromaticPitch('g', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedChromaticPitch_diatonic_pitch_number_05( ):
   '''Pitches typographically crossed.
   '''

   p1, p2 = pitchtools.NamedChromaticPitch('fss', 4), pitchtools.NamedChromaticPitch('gff', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number
