def retain_elements_at_indices_cyclic(sequence, indices, period, offset = 0):
   '''.. versionadded:: 1.1.2

   Retain `sequence` elements at `indices` mod `period` plus `offset`::

      abjad> list(seqtools.retain_elements_at_indices_cyclic(range(20), [0, 1], 5, 3))
      [3, 4, 8, 9, 13, 14, 18, 19]
   
   Ignore negative values in `indices`.

   Return generator.
   '''

   for i, element in enumerate(sequence):
      if (i - offset) % period in indices:
         yield element
