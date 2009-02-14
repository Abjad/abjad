from abjad import *


def test_halve_01( ):
   assert halve(7, bigger = 'left') == (4, 3)
   assert halve(7, bigger = 'right') == (3, 4)


def test_halve_02( ):
   assert halve(8, bigger = 'left') == (4, 4)
   assert halve(8, bigger = 'right') == (4, 4)
   assert halve(8, bigger = 'left', even = 'disallowed') == (5, 3)
   assert halve(8, bigger = 'right', even = 'disallowed') == (3, 5)
