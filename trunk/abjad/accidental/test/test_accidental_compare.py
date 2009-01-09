from abjad import *


def test_accidental_compare_01( ):
   '''Accidentals equal by string compare equally.'''
   k1, k2 = Accidental('s'), Accidental('s')
   assert     k1 == k2
   assert not k1 != k2
   assert not k1 >  k2
   assert     k1 >= k2
   assert not k1 <  k2
   assert     k1 <= k2


def test_accidental_compare_02( ):
   '''Accidentals unequal by string compare unequally.'''
   k1, k2 = Accidental('s'), Accidental('f')
   assert not k1 == k2
   assert     k1 != k2
   assert     k1 >  k2
   assert     k1 >= k2
   assert not k1 <  k2
   assert not k1 <= k2


def test_accidental_compare_03( ):
   '''No accidental and forced natural compare in a special way.'''
   k1, k2 = Accidental(''), Accidental('!')
   assert not k1 == k2
   assert     k1 != k2
   assert not k1 >  k2
   assert     k1 >= k2
   assert not k1 <  k2
   assert     k1 <= k2
