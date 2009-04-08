import math


def next_least_power_of_two(n, i = 0):
   '''Return greatest integer power of two 
      less than or equal to n.

      With i equal to 1, return the next to greatest power, etc.'''

   return 2 ** (int(math.log(n, 2)) - i)
