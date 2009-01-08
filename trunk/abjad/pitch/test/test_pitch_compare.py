from abjad import *
from py.test import raises


### TODO - Change all of this.
###        Pitches can and should order lexicographically by
###        octave, degree, accidental.adjustment

def test_pitch_compare_01( ):
   '''Pitches referentially equal.'''
   p1 = Pitch('fs', 4)
   assert     p1 == p1
   assert not p1 != p1
   assert raises (Exception, 'p1 >  p1')
   assert raises (Exception, 'p1 >= p1')
   assert raises (Exception, 'p1 <  p1')
   assert raises (Exception, 'p1 <= p1')


def test_pitch_compare_02( ):
   '''Pitches by name, accidental and octave.'''
   p1, p2 = Pitch('fs', 4), Pitch('fs', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert raises (Exception, 'p1 >  p2')
   assert raises (Exception, 'p1 >= p2')
   assert raises (Exception, 'p1 <  p2')
   assert raises (Exception, 'p1 <= p2')


def test_pitch_compare_03( ):
   '''Pitches enharmonically equal.'''
   p1, p2 = Pitch('fs', 4), Pitch('gf', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert raises (Exception, 'p1 >  p2')
   assert raises (Exception, 'p1 >= p2')
   assert raises (Exception, 'p1 <  p2')
   assert raises (Exception, 'p1 <= p2')


def test_pitch_compare_04( ):
   '''Pitches manifestly different.'''
   p1, p2 = Pitch('f', 4), Pitch('g', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert raises (Exception, 'p1 >  p2')
   assert raises (Exception, 'p1 >= p2')
   assert raises (Exception, 'p1 <  p2')
   assert raises (Exception, 'p1 <= p2')


def test_pitch_compare_05( ):
   '''Pitches typographically crossed.'''
   p1, p2 = Pitch('fss', 4), Pitch('gff', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert raises (Exception, 'p1 >  p2')
   assert raises (Exception, 'p1 >= p2')
   assert raises (Exception, 'p1 <  p2')
   assert raises (Exception, 'p1 <= p2')
