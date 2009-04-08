from abjad import *


def test_mathtools_products_01( ):
   '''Return list of the cumulative products of the elements in input.'''

   assert mathtools.products([1, 2, 3]) == [1, 2, 6]
   assert mathtools.products([10, -9, -8]) == [10, -90, 720]
   assert mathtools.products([0, 0, 0, 5]) == [0, 0, 0, 0]
   assert mathtools.products([-10, 10, -10, 10]) == [-10, -100, 1000, 10000]
