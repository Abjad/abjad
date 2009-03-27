from abjad import *
import py.test


def test_binary_string_01( ):
   '''Return base-2 representation of integer n as string.'''

   assert binary_string(1) == '1'
   assert binary_string(2) == '10'
   assert binary_string(3) == '11'
   assert binary_string(4) == '100'
   assert binary_string(5) == '101'
   assert binary_string(6) == '110'
   assert binary_string(7) == '111'
   assert binary_string(8) == '1000'


def test_binary_string_02( ):
   '''Return empty string for nonpositive integers.'''

   assert binary_string(0) == ''
   assert binary_string(-1) == ''
   assert binary_string(-2) == ''
   assert binary_string(-3) == ''


def test_binary_string_03( ):
   '''Raise TypeError for noninteger input.'''

   assert py.test.raises(TypeError, 'binary_string(5.5)')
