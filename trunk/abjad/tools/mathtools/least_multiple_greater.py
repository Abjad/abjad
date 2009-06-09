import math


def least_multiple_greater(m, n):
   '''Return the least integer multiple of *m* 
   greater than or equal to *n*.

   ::

      abjad> mathtools.least_multiple_greater(10, 47)
      50

   ::

      abjad> for m in range(1, 10):

   ::
      
      abjad> for m in range(1, 10):
      ...     print m, mathtools.least_multiple_greater(m, 47)
      ... 
      1 47
      2 48
      3 48
      4 48
      5 50
      6 48
      7 49
      8 48
      9 54

   ::

      abjad> for n in range(10, 100, 10):
      ...     print mathtools.least_multiple_greater(7, n), n
      ... 
      14 10
      21 20
      35 30
      42 40
      56 50
      63 60
      70 70
      84 80
      91 90
'''

   return m * int(math.ceil(n / float(m)))
