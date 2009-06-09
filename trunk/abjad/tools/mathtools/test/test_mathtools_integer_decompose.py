from abjad import *
import py.test


def test_integer_decompose_01( ):

   assert mathtools.integer_decompose(1) == (1, )
   assert mathtools.integer_decompose(2) == (2, )
   assert mathtools.integer_decompose(3) == (3, )
   assert mathtools.integer_decompose(4) == (4, )
   assert mathtools.integer_decompose(5) == (4, 1)
   assert mathtools.integer_decompose(6) == (6, )
   assert mathtools.integer_decompose(7) == (7, )
   assert mathtools.integer_decompose(8) == (8, )
   assert mathtools.integer_decompose(9) == (8, 1)
   assert mathtools.integer_decompose(10) == (8, 2)


def test_integer_decompose_02( ):

   assert mathtools.integer_decompose(11) == (8, 3)
   assert mathtools.integer_decompose(12) == (12, )
   assert mathtools.integer_decompose(13) == (12, 1)
   assert mathtools.integer_decompose(14) == (14, )
   assert mathtools.integer_decompose(15) == (15, )
   assert mathtools.integer_decompose(16) == (16, )
   assert mathtools.integer_decompose(17) == (16, 1)
   assert mathtools.integer_decompose(18) == (16, 2)
   assert mathtools.integer_decompose(19) == (16, 3)
   assert mathtools.integer_decompose(20) == (16, 4)


def test_mathtools_integer_decompose_03( ):

   assert py.test.raises(TypeError, 'mathtools.integer_decompose(7.5)')
   assert py.test.raises(ValueError, 'mathtools.integer_decompose(-1)')
