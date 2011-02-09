def retain_elements_at_indices_cyclically(sequence, indices, period, offset = 0):
   '''.. versionadded:: 1.1.2

   Retain `sequence` elements at `indices` mod `period` plus `offset`::

      abjad> seqtools.retain_elements_at_indices_cyclically(range(20), [0, 1], 5, 3)
      [3, 4, 8, 9, 13, 14, 18, 19]
   
   Ignore negative values in `indices`.

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.retain_elements_at_indices_cyclic( )`` to
      ``seqtools.retain_elements_at_indices_cyclically( )``.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if (i - offset) % period in indices:
         #yield element
         result.append(element)

   return result
