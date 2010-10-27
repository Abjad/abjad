def iterate_sequence_nwise_strict(iterable, n):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` `n` at a time. ::

      abjad> list(seqtools.iterate_sequence_nwise_strict(range(10), 4))
      [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8), (6, 7, 8, 9)]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.nwise_strict( )`` to
      ``seqtools.iterate_sequence_nwise_strict( )``.
   '''

   buffer = [ ]
   for element in iterable:
      buffer.append(element)
      if len(buffer) == n:
         yield tuple(buffer)
         buffer.pop(0)
