from __future__ import division
import math


def zip_cyclic(first, second):
   '''Cyclical zip. Like zip( ), but will return a list of length 
      max(len(first), len(second)) and will cycle over the elements of the
      shortest list.'''

   if not isinstance(first, (list, tuple)):
      first = [first]
   if not isinstance(second, (list, tuple)):
      second = [second]

   if len(first) > len(second):
      m = int(math.ceil(len(first) / len(second)))
      second *= m
   elif len(first) < len(second):
      m = int(math.ceil(len(second) / len(first)))
      first *= m
   return zip(first, second)
