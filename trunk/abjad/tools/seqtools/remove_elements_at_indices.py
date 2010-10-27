def remove_elements_at_indices(iterable, indices):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` except those at `indices`. ::

      abjad> list(seqtools.remove_elements_at_indices(range(20), [1, 16, 17, 18]))
      [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19]

   Negative indices are ignored.
   '''

   for i, element in enumerate(iterable):
      if i not in indices:
         yield element
