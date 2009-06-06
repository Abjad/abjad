from __future__ import division
import math


def zip_cyclic(first, second):
   '''Like Python :func:`zip`, but return a list of length 
   ``max(len(first), len(second))`` and cycle over the elements of the
   shorter list.

   ::

      abjad> listtools.zip_cyclic([1, 2, 3], ['a', 'b'])
      [(1, 'a'), (2, 'b'), (3, 'a')]

   .. todo:: Generalize to any number of input lists.'''

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
