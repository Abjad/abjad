from abjad import *
from py.test import raises


def test_rest_compare_01( ):
   '''Rests referentially equal.'''
   r1 = Rest((1, 4))
   assert     r1 == r1
   assert not r1 != r1
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')


def test_rest_compare_02( ):
   '''Rests superficially similar.'''
   r1 = Rest((1, 4))
   r2 = Rest((1, 4))
   assert not r1 == r2
   assert     r1 != r2
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')


def test_rest_compare_03( ):
   '''Rests manifestly different.'''
   r1 = Rest((1, 4))
   r2 = Rest((1, 8))
   assert not r1 == r2
   assert     r1 != r2
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')
