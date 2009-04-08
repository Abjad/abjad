from abjad import *


def test_mathtools_integer_halve_01( ):
   assert mathtools.integer_halve(7, bigger = 'left') == (4, 3)
   assert mathtools.integer_halve(7, bigger = 'right') == (3, 4)


def test_mathtools_integer_halve_02( ):
   assert mathtools.integer_halve(8, bigger = 'left') == (4, 4)
   assert mathtools.integer_halve(8, bigger = 'right') == (4, 4)
   assert mathtools.integer_halve(8, bigger = 'left', even = 'disallowed') == (5, 3)
   assert mathtools.integer_halve(8, bigger = 'right', even = 'disallowed') == (3, 5)
