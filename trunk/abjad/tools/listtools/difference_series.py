def difference_series(l):
   '''Yield differences of adjacent elements in iterable `l`.

   ::

      abjad> l = [1, 1, 2, 3, 5, 5, 6]
      abjad> list(listtools.difference_series(l))
      [0, 1, 1, 2, 0, 1]
   '''

   for i, n in enumerate(l[1:]):
      yield n - l[i]
