def remove_sequence_elements_at_indices_cyclically(sequence, indices, period, offset = 0):
   '''.. versionadded:: 1.1.2

   Remove `sequence` elements at `indices` mod `period` plus `offset`::

      abjad> seqtools.remove_sequence_elements_at_indices(range(20), [0, 1], 5, 3)
      [0, 1, 2, 5, 6, 7, 10, 11, 12, 15, 16, 17]

   Ignore negative indices.

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.remove_sequence_elements_at_indices_cyclic( )`` to
      ``seqtools.remove_sequence_elements_at_indices_cyclically( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.remove_elements_at_indices_cyclically( )`` to
      ``seqtools.remove_sequence_elements_at_indices_cyclically( )``.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if (i - offset) % period not in indices:
         #yield element
         result.append(element)

   return result
