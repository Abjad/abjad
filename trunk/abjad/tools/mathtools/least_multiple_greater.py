import math


def least_multiple_greater(m, n):
   '''Return the least multiple of m greater than *or equal to* n.

   mathtools.least_multiple_greater(10, 89)
   90

   mathtools.least_multiple_greater(7, 70)
   70'''

   return m * int(math.ceil(n / float(m)))
