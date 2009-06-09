from abjad import *
import py.test


def test_mathtools_integer_halve_01( ):
   assert mathtools.integer_halve(7, bigger = 'left') == (4, 3)
   assert mathtools.integer_halve(7, bigger = 'right') == (3, 4)


def test_mathtools_integer_halve_02( ):
   assert mathtools.integer_halve(8, bigger = 'left') == (4, 4)
   assert mathtools.integer_halve(8, bigger = 'right') == (4, 4)
   assert mathtools.integer_halve(8, bigger = 'left', even = 'disallowed') == (5, 3)
   assert mathtools.integer_halve(8, bigger = 'right', even = 'disallowed') == (3, 5)


def test_mathtools_integer_halve_03( ):
   '''Raise TypeError on noninteger n.
      Raise ValueError on nonpositive n.'''

   assert py.test.raises(TypeError, "mathtools.integer_halve('foo')")
   assert py.test.raises(ValueError, 'mathtools.integer_halve(-1)')
