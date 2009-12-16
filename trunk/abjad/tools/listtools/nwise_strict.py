def nwise_strict(iterable, n):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` `n` at a time. ::

      abjad> list(listtools.nwise_strict(range(10), 4))
      [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8), (6, 7, 8, 9)]
   '''

   buffer = [ ]
   for element in iterable:
      buffer.append(element)
      if len(buffer) == n:
         yield tuple(buffer)
         buffer.pop(0)
