def repeat_sequence_elements_at_indices(sequence, indices, total):
   '''.. versionadded:: 1.1.2

   Repeat `sequence` elements at `indices` to `total` length::

      abjad> seqtools.repeat_sequence_elements_at_indices(range(10), [6, 7, 8], 3)
      [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.repeat_elements_at_indices( )`` to
      ``seqtools.repeat_sequence_elements_at_indices( )``.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if i in indices:
         #yield total * [element]
         result.append(total * [element])
      else:
         #yield element
         result.append(element)

   return result
