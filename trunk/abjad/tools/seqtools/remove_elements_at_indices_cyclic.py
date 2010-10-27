def remove_elements_at_indices_cyclic(iterable, indices, period, offset = 0):
   '''.. versionadded:: 1.1.2

   Yield elements ``iterable[i]`` except those for which
   ``(i - offset) % period`` is in `indices`. ::

      abjad> list(seqtools.remove_elements_at_indices(range(20), [0, 1], 5, 3)
      [0, 1, 2, 5, 6, 7, 10, 11, 12, 15, 16, 17]

   Negative indices are ignored.
   '''

   for i, element in enumerate(iterable):
      if (i - offset) % period not in indices:
         yield element
