import math


def _greatest_multiple_less(m, n):
   '''Return the greatest multiple of m less than *or equal to* n.'''

   return m * int(math.floor(n / float(m)))
