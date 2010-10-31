def repeat_elements_at_indices(sequence, indices, total):
   '''.. versionadded:: 1.1.2

   Repeat `sequence` elements at `indices` to `total` length::

      abjad> list(seqtools.repeat_elements_at_indices(range(10), [6, 7, 8], 3))
      [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]

   Return generator.
   '''

   for i, element in enumerate(sequence):
      if i in indices:
         yield total * [element]
      else:
         yield element
