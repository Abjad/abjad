from abjad.tools.seqtools.flatten_sequence import flatten_sequence


def increase_elements_at_indices_by_addenda(sequence, addenda, indices):
   '''Increase `sequence` by `addenda` at `indices`::

      abjad> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
      abjad> seqtools.increase_elements_at_indices_by_addenda(sequence, [0.5, 0.5], [0, 4, 8])
      [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.increase_at_indices( )`` to
      ``seqtools.increase_elements_at_indices_by_addenda( )``.
   '''

   # assert no overlaps
   tmp = flatten_sequence([range(i, len(addenda)) for i in indices])
   assert len(tmp) == len(set(tmp))

   result = sequence[:]

   for i in indices:
      for j in range(len(addenda)):
         result[i+j] += addenda[j]

   return result
