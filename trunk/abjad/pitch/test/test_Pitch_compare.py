from abjad import *
import py.test


def test_Pitch_compare_01( ):
   '''Referentially equal pitches compare equally.'''
   p1 = Pitch('fs', 4)
   assert     p1 == p1
   assert not p1 != p1
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_02( ):
   '''Pitches equal by name, accidental and octave compare equally.'''
   p1, p2 = Pitch('fs', 4), Pitch('fs', 4)
   assert     p1 == p2
   assert not p1 != p2
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_03( ):
   '''Pitches enharmonically equal compare unequally.'''
   p1, p2 = Pitch('fs', 4), Pitch('gf', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_04( ):
   '''Pitches manifestly different compare unequally.'''
   p1, p2 = Pitch('f', 4), Pitch('g', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_05( ):
   '''Pitches typographically crossed compare unequally.'''
   p1, p2 = Pitch('fss', 4), Pitch('gff', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_06( ):
   '''Pitches test False for equality against unlike instances.
      Other pitch comparisons raise ValueError against unlike instances.'''
   p = Pitch('c', 4)
   n = 99
   assert not p == n
   assert     p != n
   assert py.test.raises(ValueError, 'p >  n')
   assert py.test.raises(ValueError, 'p >= n')
   assert py.test.raises(ValueError, 'p <  n')
   assert py.test.raises(ValueError, 'p <= n')


def test_Pitch_compare_07( ):
   '''Pitches with like name, accidental, octave and deviation
      compare equally.'''
   p1 = Pitch('bf', 4, -31)
   p2 = Pitch('bf', 4, -31)
   assert     p1 == p2
   assert not p1 != p2
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_08( ):
   '''Pitches with like name, accidental and ocatve
      but with different deviation compare unequally.'''
   p1 = Pitch('bf', 4, 0)
   p2 = Pitch('bf', 4, -31)
   assert not p1 == p2
   assert     p1 != p2
   assert     p1 >  p2
   assert     p1 >= p2
   assert not p1 <  p2
   assert not p1 <= p2


def test_Pitch_compare_09( ):
   '''Pitches with the same frequency but with different deviation
      do not compare equally.'''
   p1 = Pitch('c', 5)
   p2 = Pitch('bf', 4, 100)
   assert not p1 == p2
   assert     p1 != p2
   assert     p1 >  p2
   assert     p1 >= p2
   assert not p1 <  p2
   assert not p1 <= p2
