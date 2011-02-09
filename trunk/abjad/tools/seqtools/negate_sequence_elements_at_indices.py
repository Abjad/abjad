def negate_sequence_elements_at_indices(sequence, indices, period = None):
   '''Negate `sequence` elements at `indices`::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.negate_sequence_elements_at_indices(l, [0, 1, 2])
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   Negate `sequence` elements at `indices` cyclically according to `period`::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.negate_sequence_elements_at_indices(l, [0, 1, 2], period = 5)
      [-1, -2, -3, 4, 5, 6, 7, -8, -9, -10]

   Return newly constructed list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.negate_elements_at_indices( )`` to
      ``seqtools.negate_sequence_elements_at_indices( )``.
   '''
   
   if not isinstance(sequence, list):
      raise TypeError

   result = [ ]

   for i, element in enumerate(sequence):
      if (i in indices) or (period and i % period in indices):
         result.append(-element)
      else:
         result.append(element)

   return result
