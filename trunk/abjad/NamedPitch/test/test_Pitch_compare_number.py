from abjad import *
from py.test import raises


def test_Pitch_compare_number_01( ):
   '''Pitches referentially equal.'''
   p1 = NamedPitch('fs', 4)
   assert     p1.number == p1.number
   assert not p1.number != p1.number
   assert not p1.number >  p1.number
   assert     p1.number >= p1.number
   assert not p1.number <  p1.number
   assert     p1.number <= p1.number


def test_Pitch_compare_number_02( ):
   '''Pitches by name, accidental and octave.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('fs', 4)
   assert     p1.number == p2.number
   assert not p1.number != p2.number
   assert not p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert     p1.number <= p2.number


def test_Pitch_compare_number_03( ):
   '''Pitches enharmonically equal.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('gf', 4)
   assert     p1.number == p2.number
   assert not p1.number != p2.number
   assert not p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert     p1.number <= p2.number


def test_Pitch_compare_number_04( ):
   '''Pitches manifestly different.'''
   p1, p2 = NamedPitch('f', 4), NamedPitch('g', 4)
   assert not p1.number == p2.number
   assert     p1.number != p2.number
   assert not p1.number >  p2.number
   assert not p1.number >= p2.number
   assert     p1.number <  p2.number
   assert     p1.number <= p2.number


def test_Pitch_compare_number_05( ):
   '''Pitches typographically crossed.'''
   p1, p2 = NamedPitch('fss', 4), NamedPitch('gff', 4)
   assert not p1.number == p2.number
   assert     p1.number != p2.number
   assert     p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert not p1.number <= p2.number
