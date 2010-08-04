from abjad import *
from py.test import raises


def test_NamedPitch_compare_altitude_01( ):
   '''Pitches referentially equal.'''
   p1 = NamedPitch('fs', 4)
   assert     p1.altitude == p1.altitude
   assert not p1.altitude != p1.altitude
   assert not p1.altitude >  p1.altitude
   assert     p1.altitude >= p1.altitude
   assert not p1.altitude <  p1.altitude
   assert     p1.altitude <= p1.altitude


def test_NamedPitch_compare_altitude_02( ):
   '''Pitches by name, accidental and octave.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('fs', 4)
   assert     p1.altitude == p2.altitude
   assert not p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert     p1.altitude >= p2.altitude
   assert not p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_NamedPitch_compare_altitude_03( ):
   '''Pitches enharmonically equal.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('gf', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_NamedPitch_compare_altitude_04( ):
   '''Pitches manifestly different.'''
   p1, p2 = NamedPitch('f', 4), NamedPitch('g', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude


def test_NamedPitch_compare_altitude_05( ):
   '''Pitches typographically crossed.'''
   p1, p2 = NamedPitch('fss', 4), NamedPitch('gff', 4)
   assert not p1.altitude == p2.altitude
   assert     p1.altitude != p2.altitude
   assert not p1.altitude >  p2.altitude
   assert not p1.altitude >= p2.altitude
   assert     p1.altitude <  p2.altitude
   assert     p1.altitude <= p2.altitude
