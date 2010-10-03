from abjad import *


def test_NamedPitch_diatonic_pitch_number_01( ):
   '''Pitches referentially equal.
   '''

   p1 = pitchtools.NamedPitch('fs', 4)

   assert     p1.diatonic_pitch_number == p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number != p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p1.diatonic_pitch_number
   assert     p1.diatonic_pitch_number >= p1.diatonic_pitch_number
   assert not p1.diatonic_pitch_number <  p1.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p1.diatonic_pitch_number


def test_NamedPitch_diatonic_pitch_number_02( ):
   '''Pitches by name, accidental and octave.
   '''

   p1, p2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('fs', 4)

   assert     p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedPitch_diatonic_pitch_number_03( ):
   '''Pitches enharmonically equal.
   '''

   p1, p2 = pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('gf', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedPitch_diatonic_pitch_number_04( ):
   '''Pitches manifestly different.
   '''

   p1, p2 = pitchtools.NamedPitch('f', 4), pitchtools.NamedPitch('g', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number


def test_NamedPitch_diatonic_pitch_number_05( ):
   '''Pitches typographically crossed.
   '''

   p1, p2 = pitchtools.NamedPitch('fss', 4), pitchtools.NamedPitch('gff', 4)

   assert not p1.diatonic_pitch_number == p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number != p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >  p2.diatonic_pitch_number
   assert not p1.diatonic_pitch_number >= p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <  p2.diatonic_pitch_number
   assert     p1.diatonic_pitch_number <= p2.diatonic_pitch_number
