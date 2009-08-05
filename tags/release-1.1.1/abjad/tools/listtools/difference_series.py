def difference_series(l):
   '''Return generator of differences of adjacent elements in l.

      >>> l = [1, 1, 2, 3, 5, 5, 6]
      >>> list(listtools.difference_series(l))
      [0, 1, 1, 2, 0, 1]'''

   for i, n in enumerate(l[1:]):
      yield n - l[i]
