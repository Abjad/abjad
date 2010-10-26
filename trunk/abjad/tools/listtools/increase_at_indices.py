from abjad.tools.listtools.flatten_sequence import flatten_sequence


def increase_at_indices(l, addenda, indices):
   '''Increase the elements of list ``l`` by the elements
   of ``addenda`` at ``indices`` in ``l``.

   ::

      abjad> l = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
      abjad> listtools.increase_at_indices(l, [0.5, 0.5], [0, 4, 8])
      [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]
   '''

   # assert no overlaps
   tmp = flatten_sequence([range(i, len(addenda)) for i in indices])
   assert len(tmp) == len(set(tmp))

   result = l[:]

   for i in indices:
      for j in range(len(addenda)):
         result[i+j] += addenda[j]

   return result
