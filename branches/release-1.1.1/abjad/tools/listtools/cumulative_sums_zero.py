def cumulative_sums_zero(l):
   '''Return a list of the cumulative sums of the elements in *l*,
   starting with ``0``.

   .. note:: ``len(listtools.cumulative_sums_zero(l)) == len(l) + 1``.

   ::

      abjad> listtools.cumulative_sums_zero([1, 2, 3, 4, 5, 6, 7, 8])
      [0, 1, 3, 6, 10, 15, 21, 28, 36]

   ::
   
      abjad> listtools.cumulative_sums_zero([1, -2, 3, -4, 5, -6, 7, -8])
      [0, 1, -1, 2, -2, 3, -3, 4, -4]

   Raise :exc:`ValueError` when *l* is empty::

      abjad> listtools.cumulative_sums_zero([ ])
      ValueError'''

   result = [0]
   for element in l:
      result.append(result[-1] + element) 

   return result
