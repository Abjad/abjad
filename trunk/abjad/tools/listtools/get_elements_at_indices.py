def get_elements_at_indices(iterable, indices):
   '''.. versionadded:: 1.1.2

   Get elements at `indices` in `iterable`.
   '''

   for i, element in enumerate(iterable):
      if i in indices:
         yield element
