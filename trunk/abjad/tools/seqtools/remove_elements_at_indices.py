def remove_elements_at_indices(sequence, indices):
   '''.. versionadded:: 1.1.2

   Remove `sequence` elements at `indices`::

      abjad> list(seqtools.remove_elements_at_indices(range(20), [1, 16, 17, 18]))
      [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19]

   Ignore negative indices.

   Return generator.
   '''

   for i, element in enumerate(sequence):
      if i not in indices:
         yield element
