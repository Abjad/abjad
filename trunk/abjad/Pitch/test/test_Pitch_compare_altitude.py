from abjad import *
from py.test import raises


def test_Pitch_compare_altitude_01( ):
   '''Pitches referentially equal.'''
   p1 = Pitch('fs', 4)
   assert     p1.altitude == p1.altitude
   assert not p1.altitude != p1.altitude
   assert not p1.altitude >  p1.altitude
   assert     p1.altitude >= p1.altitude
   assert not p1.altitude <  p1.altitude
   assert     p1.altitude <= p1.altitude


def test_Pitch_compare_altitude_02( ):
   '''Pitches by name, accidental and octave.'''
   p1, p2 = Pitch('fs', 4), Pitch('fs', 4)
   assert     p1.altitude == p2.altitude
   assert not p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert     p1.altitude >= p2.altitude
   assert not p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_Pitch_compare_altitude_03( ):
   '''Pitches enharmonically equal.'''
   p1, p2 = Pitch('fs', 4), Pitch('gf', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_Pitch_compare_altitude_04( ):
   '''Pitches manifestly different.'''
   p1, p2 = Pitch('f', 4), Pitch('g', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_Pitch_compare_altitude_05( ):
   '''Pitches typographically crossed.'''
   p1, p2 = Pitch('fss', 4), Pitch('gff', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude
