def retain_elements_at_indices(sequence, indices):
   '''.. versionadded:: 1.1.2

   Retain `sequence` elements at `indices`::

      abjad> list(seqtools.retain_elements_at_indices(range(20), [1, 16, 17, 18]))
      [1, 16, 17, 18]

   Ignore negative indices.

   Return generator.
   '''

   for i, element in enumerate(sequence):
      if i in indices:
         yield element
