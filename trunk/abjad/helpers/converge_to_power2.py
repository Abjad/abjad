import math
from .. duration.rational import Rational

def converge_to_power2(source, target):
   '''Returns the number 2**n closest to target i.e. min(2**n - target)
      "coming from the direction of source". i.e. if source < target
      the function returns 2**n < target. If source > target, it returns
      2**n greater than target.

      Example:

      abjad> for x in range(1, 20):
      ...     print x, converge_to_power2(0, x), converge_to_power2(10000, x)
      ...
      1 1 1
      2 2 2
      3 2 4
      4 4 4
      5 4 8
      6 4 8
      7 4 8
      8 8 8
      9 8 16
      10 8 16
      11 8 16
      12 8 16
      13 8 16
      14 8 16
      15 8 16
      16 16 16
      17 16 32
      18 16 32
      19 16 32
      '''
   if source < target:
      return Rational(2) ** int(math.floor(math.log(target, 2)))
   elif source > target:
      return Rational(2) ** int(math.ceil(math.log(target, 2)))
   else:
      return source
