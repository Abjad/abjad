def pairs_from_to(l, m):
   '''.. versionadded:: 1.1.2

   Yield pairs from `l` to `m`. ::

      abjad> for pair in listtools.pairs_from_to([1, 2, 3], [4, 5]):
      ...     pair 
      ... 
      (1, 4)
      (1, 5)
      (2, 4)
      (2, 5)
      (3, 4)
      (3, 5)
   '''

   for x in l:
      for y in m:
         yield x, y
