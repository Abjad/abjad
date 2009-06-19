import math


def greatest_multiple_less_equal(m, n):
   '''Return the greatest integer multiple of `m` 
   less than or equal to `n`::

      abjad> mathtools.greatest_multiple_less_equal(10, 47)
      40

   ::

      abjad> for m in range(1, 10):
      ...     print m, mathtools.greatest_multiple_less_equal(m, 47)
      ... 
      1 47
      2 46
      3 45
      4 44
      5 45
      6 42
      7 42
      8 40
      9 45

   ::

      abjad> for n in range(10, 100, 10):
      ...     print mathtools.greatest_multiple_less_equal(7, n), n
      ... 
      7 10
      14 20
      28 30
      35 40
      49 50
      56 60
      70 70
      77 80
      84 90'''

   return m * int(math.floor(n / float(m)))
