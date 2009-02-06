import math


def _next_least_power_of_two(n):
   '''Return greatest integer power of two 
      less than or equal to n.'''

   return 2 ** int(math.log(n, 2))
