from abjad import *
import py.test


def test_Pitch_compare_01( ):
   '''Referentially equal pitches compare equally.'''
   p1 = NamedPitch('fs', 4)
   assert     p1 == p1
   assert not p1 != p1
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_02( ):
   '''Pitches equal by name, accidental and octave compare equally.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('fs', 4)
   assert     p1 == p2
   assert not p1 != p2
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_03( ):
   '''Pitches enharmonically equal compare unequally.'''
   p1, p2 = NamedPitch('fs', 4), NamedPitch('gf', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_04( ):
   '''Pitches manifestly different compare unequally.'''
   p1, p2 = NamedPitch('f', 4), NamedPitch('g', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_05( ):
   '''Pitches typographically crossed compare unequally.'''
   p1, p2 = NamedPitch('fss', 4), NamedPitch('gff', 4)
   assert not p1 == p2
   assert     p1 != p2
   assert not p1 >  p2
   assert not p1 >= p2
   assert     p1 <  p2
   assert     p1 <= p2


def test_Pitch_compare_06( ):
   '''Pitches test False for equality against unlike instances.
      Other pitch comparisons raise ValueError against unlike instances.'''
   p = NamedPitch('c', 4)
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
   p1 = NamedPitch('bf', 4, -31)
   p2 = NamedPitch('bf', 4, -31)
   assert     p1 == p2
   assert not p1 != p2
   assert not p1 >  p1
   assert     p1 >= p1
   assert not p1 <  p1
   assert     p1 <= p1


def test_Pitch_compare_08( ):
   '''Pitches with like name, accidental and ocatve
      but with different deviation compare unequally.'''
   p1 = NamedPitch('bf', 4, 0)
   p2 = NamedPitch('bf', 4, -31)
   assert not p1 == p2
   assert     p1 != p2
   assert     p1 >  p2
   assert     p1 >= p2
   assert not p1 <  p2
   assert not p1 <= p2


def test_Pitch_compare_09( ):
   '''Pitches with the same frequency but with different deviation
      do not compare equally.'''
   p1 = NamedPitch('c', 5)
   p2 = NamedPitch('bf', 4, 100)
   assert not p1 == p2
   assert     p1 != p2
   assert     p1 >  p2
   assert     p1 >= p2
   assert not p1 <  p2
   assert not p1 <= p2
