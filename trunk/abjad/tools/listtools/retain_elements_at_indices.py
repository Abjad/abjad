def retain_elements_at_indices(iterable, indices):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` at `indices`. ::

      abjad> list(listtools.retain_elements_at_indices(range(20), [1, 16, 17, 18]))
      [1, 16, 17, 18]

   Negative indices are ignored.
   '''

   for i, element in enumerate(iterable):
      if i in indices:
         yield element
