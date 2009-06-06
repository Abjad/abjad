def negate_elements_at_indices(l, indices, period = None):
   '''Negate elements in ``l`` at ``indices``.
   When ``period`` is a positive integer, read ``indices`` 
   cyclically according to ``period``.

   ::

      >>> l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      >>> listtools.negate_elements_at_indices(l, [0, 1, 2], None)
      [-1, -2, -3, 4, 5, 6, 7, 8, 9, 10]

   ::

      >>> l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      >>> listtools.negate_elements_at_indices(l, [0, 1, 2], 5)
      [-1, -2, -3, 4, 5, -6, -7, -8, 9, 10]'''

   
   result = [ ]

   for i, element in enumerate(l):
      if (i in indices) or (period and i % period in indices):
         result.append(-element)
      else:
         result.append(element)

   return result
