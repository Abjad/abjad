from abjad import *
import py.test


## TODO: Port forward to new style of tests. ##

## TEST TYPICAL DIVIDE ##

def test_divide_pair_01( ):
   t = divide.pair([1, 2, 4], (6, 16))
   assert str(t) == "{@ 7:6 c'16, c'8, c'4 @}"

def test_divide_pair_02( ):
   t = divide.pair([1, 1, 2, 4], (6, 16))
   assert str(t) == "{@ 4:3 c'16, c'16, c'8, c'4 @}"

def test_divide_pair_03( ):
   t = divide.pair([-2, 3, 7], (7, 16))
   assert str(t) == "{@ 12:7 r8, c'8., c'4.. @}"

def test_divide_pair_04( ):
   t = divide.pair([7, 7, -4, -1], (1, 4))
   assert str(t) == "{@ 19:16 c'16.., c'16.., r16, r64 @}"


## TEST DIVIDE, DOUBLE LIST ##

def test_divide_pair_05( ):
   t = divide.pair([1, 2, 2], (12, 16))
   assert str(t) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_divide_pair_06( ):
   t = divide.pair([2, 4, 4], (12, 16))
   assert str(t) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_divide_pair_07( ):
   t = divide.pair([4, 8, 8], (12, 16))
   assert str(t) == "{@ 5:3 c'4, c'2, c'2 @}"

def test_divide_pair_08( ):
   t = divide.pair([8, 16, 16], (12, 16))
   assert str(t) == "{@ 5:3 c'4, c'2, c'2 @}"


## TEST DIVIDE, DOUBLE NUMERATOR ##

def test_divide_pair_09( ):
   t = divide.pair([2, 4, 4], (3, 16))
   assert str(t) == "{@ 5:3 c'16, c'8, c'8 @}"

def test_divide_pair_10( ):
   t = divide.pair([2, 4, 4], (6, 16))
   assert str(t) == "{@ 5:3 c'8, c'4, c'4 @}"

def test_divide_pair_11( ):
   t = divide.pair([2, 4, 4], (12, 16))
   assert str(t) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_divide_pair_12( ):
   t = divide.pair([2, 4, 4], (24, 16))
   assert str(t) == "{@ 5:6 c'4, c'2, c'2 @}"


## TEST DIVIDE, DOUBLE DENOMINATOR ##

def test_divide_pair_13( ):
   t = divide.pair([1, 2, 2], (6, 2))
   assert str(t) == "{@ 5:6 c'2, c'1, c'1 @}"

def test_divide_pair_14( ):
   t = divide.pair([1, 2, 2], (6, 4))
   assert str(t) == "{@ 5:6 c'4, c'2, c'2 @}"

def test_divide_pair_15( ):
   t = divide.pair([1, 2, 2], (6, 8))
   assert str(t) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_divide_pair_16( ):
   t = divide.pair([1, 2, 2], (6, 16))
   assert str(t) == "{@ 5:6 c'16, c'8, c'8 @}"


## TEST DIVIDE, NO PROLATION ##

def test_divide_pair_17( ):
   t = divide.pair([1, -1, -1], (3, 16))
   assert str(t) == "{@ 1:1 c'16, r16, r16 @}"

def test_divide_pair_18( ):
   t = divide.pair([1, 1, -1, -1], (4, 16))
   assert str(t) == "{@ 1:1 c'16, c'16, r16, r16 @}" 

def test_divide_pair_19( ):
   t = divide.pair([1, 1, 1, -1, -1], (5, 16))
   assert str(t) == "{@ 1:1 c'16, c'16, c'16, r16, r16 @}"

def test_divide_pair_20( ):
   t = divide.pair([1, 1, 1, 1, -1, -1], (6, 16))
   assert str(t) == "{@ 1:1 c'16, c'16, c'16, c'16, r16, r16 @}"


## TEST LONE DIVIDE ##

def test_divide_pair_21( ):
   t = divide.pair([1], (6, 16))
   assert str(t) == "{c'4.}"

def test_divide_pair_22( ):
   t = divide.pair([99], (6, 16))
   assert str(t) == "{c'4.}"

def test_divide_pair_23( ):
   t = divide.pair([-1], (6, 16))
   assert str(t) == "{r4.}"

def test_divide_pair_24( ):
   t = divide.pair([-99], (6, 16))
   assert str(t) == "{r4.}"


## TEST DIVIDE ASSERTIONS ##

def test_divide_pair_25( ):
   py.test.raises(ValueError, 'divide.pair([ ], (3, 16))')

def test_divide_pair_26( ):
   py.test.raises(ValueError, 'divide.pair([0], (3, 16))')

def test_divide_pair_27( ):
   py.test.raises(ValueError, 'divide.pair([1, 1, 0, 1], (3, 16))')
