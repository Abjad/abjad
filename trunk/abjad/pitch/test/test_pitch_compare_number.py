from abjad import *
from py.test import raises


def test_pitch_compare_number_01( ):
   '''Pitches referentially equal.'''
   p1 = Pitch('fs', 4)
   assert     p1.number == p1.number
   assert not p1.number != p1.number
   assert not p1.number >  p1.number
   assert     p1.number >= p1.number
   assert not p1.number <  p1.number
   assert     p1.number <= p1.number


def test_pitch_compare_number_02( ):
   '''Pitches by name, accidental and octave.'''
   p1, p2 = Pitch('fs', 4), Pitch('fs', 4)
   assert     p1.number == p2.number
   assert not p1.number != p2.number
   assert not p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert     p1.number <= p2.number


def test_pitch_compare_number_03( ):
   '''Pitches enharmonically equal.'''
   p1, p2 = Pitch('fs', 4), Pitch('gf', 4)
   assert     p1.number == p2.number
   assert not p1.number != p2.number
   assert not p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert     p1.number <= p2.number


def test_pitch_compare_number_04( ):
   '''Pitches manifestly different.'''
   p1, p2 = Pitch('f', 4), Pitch('g', 4)
   assert not p1.number == p2.number
   assert     p1.number != p2.number
   assert not p1.number >  p2.number
   assert not p1.number >= p2.number
   assert     p1.number <  p2.number
   assert     p1.number <= p2.number


def test_pitch_compare_number_05( ):
   '''Pitches typographically crossed.'''
   p1, p2 = Pitch('fss', 4), Pitch('gff', 4)
   assert not p1.number == p2.number
   assert     p1.number != p2.number
   assert     p1.number >  p2.number
   assert     p1.number >= p2.number
   assert not p1.number <  p2.number
   assert not p1.number <= p2.number
