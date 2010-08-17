from abjad import *
from py.test import raises


def test_MultiMeasureRest_compare_01( ):
   '''Multi-measure rests referentially equal.'''
   r1 = resttools.MultiMeasureRest((1, 4))
   assert     r1 == r1
   assert not r1 != r1
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')


def test_MultiMeasureRest_compare_02( ):
   '''Multi-measure rests superficially similar.'''
   r1 = resttools.MultiMeasureRest((1, 4))
   r2 = resttools.MultiMeasureRest((1, 4))
   assert not r1 == r2
   assert     r1 != r2
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')


def test_MultiMeasureRest_compare_03( ):
   '''Multi-measure rests manifestly different.'''
   r1 = resttools.MultiMeasureRest((1, 4))
   r2 = resttools.MultiMeasureRest((1, 8))
   assert not r1 == r2
   assert     r1 != r2
   assert raises(Exception, 'r1 >  r1')
   assert raises(Exception, 'r1 >= r1')
   assert raises(Exception, 'r1 <  r1')
   assert raises(Exception, 'r1 <= r1')
