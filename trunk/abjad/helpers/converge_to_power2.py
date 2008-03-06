import math
from .. duration.rational import Rational

def converge_to_power2(source, target):
   '''Returns the number 2**n closest to target i.e. min(2**n - target)
      "coming from the direction of source". i.e. if source < target
      the function returns 2**n < target. If source > target, it returns
      2**n greater than target.'''
   if source < target:
      return Rational(2) ** int(math.floor(math.log(target, 2)))
   elif source > target:
      return Rational(2) ** int(math.ceil(math.log(target, 2)))
   else:
      return source
