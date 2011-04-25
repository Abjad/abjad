def iterate_sequence_nwise_strict(sequence, n):
   '''.. versionadded:: 1.1.2

   Iterate elements in `sequence` `n` at a time::

      abjad> list(seqtools.iterate_sequence_nwise_strict(range(10), 4))
      [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8), (6, 7, 8, 9)]

   Return generator.
   '''

   buffer = [ ]
   for element in sequence:
      buffer.append(element)
      if len(buffer) == n:
         yield tuple(buffer)
         buffer.pop(0)
