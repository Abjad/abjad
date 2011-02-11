def negate_absolute_value_of_sequence_elements_at_indices(sequence, indices, period = None):
   '''Negate the absolute value of `sequence` elements at `indices`::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.flip_sign_of_sequence_elements_at_indices(l, [0, 1, 2], period = None)
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   Negate the absolute value of `sequence` elements at `indices` cyclically
   according to `period`::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.flip_sign_of_sequence_elements_at_indices(l, [0, 1, 2], period = 5)
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   Return newly constructed list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.negate_elements_at_indices_absolutely( )`` to
      ``seqtools.flip_sign_of_sequence_elements_at_indices_absolutely( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.negate_sequence_elements_at_indices_absolutely( )`` to
      ``seqtools.negate_absolute_value_of_sequence_elements_at_indices( )``.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if (i in indices) or (period and i % period in indices):
         result.append(-abs(element))
      else:
         result.append(element)

   return result
