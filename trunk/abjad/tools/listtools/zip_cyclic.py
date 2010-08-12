from __future__ import division
import math


def zip_cyclic(*iterables):
   '''Like Python :func:`zip`, but return a list of length equal
   to the iterable of greatest length in `iterables` and cycle
   over the elements of the iterables of shorter length. ::

      abjad> listtools.zip_cyclic([1, 2, 3], ['a', 'b'])
      [(1, 'a'), (2, 'b'), (3, 'a')]

   .. versionadded:: 1.1.1
      Arbitrary number of input iterables now allowed.

   ::

      abjad> a = [10, 11, 12]
      abjad> b = [20, 21]
      abjad> c = [30, 31, 32, 33]
      abjad> listtools.zip_cyclic(a, b, c)
      [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]
   '''

   ## make sure iterables are, in fact, all iterables
   new_iterables = [ ]
   for iterable in iterables:
      if not isinstance(iterable, (list, tuple)):
         new_iterables.append([iterable])
      else:
         new_iterables.append(iterable)

   ## find length of longest iterable
   max_length = max([len(x) for x in new_iterables])

   ## produce list of tuples
   result = [ ] 
   for i in range(max_length):
      part = [x[i % len(x)] for x in new_iterables]
      result.append(tuple(part))

   ## return result
   return result
