from abjad.helpers.factors import _factors
from py.test import raises

def test_factors_01( ):
   assert raises(AssertionError, '_factors(0)')
   assert raises(AssertionError, '_factors(1)')
   
def test_factors_02( ):
   t = _factors(2)
   assert t == [2]
   
def test_factors_03( ):
   t = _factors(3)
   assert t == [3]
   
def test_factors_04( ):
   t = _factors(4)
   assert t == [2, 2]
   
def test_factors_05( ):
   t = _factors(6)
   assert t == [2, 3]
   
def test_factors_06( ):
   t = _factors(12)
   assert t == [2, 2, 3]
   
