def retain_elements_at_indices_cyclic(iterable, indices, period, offset = 0):
   '''.. versionadded:: 1.1.2

   Yield elements ``iterable[i]`` such that
   ``(i - offset) % period`` is in `indices`. ::

      abjad> list(seqtools.retain_elements_at_indices_cyclic(range(20), [0, 1], 5, 3))
      [3, 4, 8, 9, 13, 14, 18, 19]
   
   Negative indices are ignored.
   '''

   for i, element in enumerate(iterable):
      if (i - offset) % period in indices:
         yield element
