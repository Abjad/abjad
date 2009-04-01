from abjad.tools import mathtools
import py.test

def test_factors_01( ):
   assert py.test.raises(AssertionError, 'mathtools.factors(0)')
   
def test_factors_03( ):
   t = mathtools.factors(2)
   assert t == [1]

def test_factors_03( ):
   t = mathtools.factors(2)
   assert t == [1, 2]
   
def test_factors_04( ):
   t = mathtools.factors(3)
   assert t == [1, 3]
   
def test_factors_05( ):
   t = mathtools.factors(4)
   assert t == [1, 2, 2]
   
def test_factors_06( ):
   t = mathtools.factors(6)
   assert t == [1, 2, 3]
   
def test_factors_07( ):
   t = mathtools.factors(12)
   assert t == [1, 2, 2, 3]
