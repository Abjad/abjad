def get_sequence_elements_at_indices(sequence, indices):
   '''.. versionadded:: 1.1.2

   Get `sequence` elements at `indices`::

      abjad> seqtools.get_sequence_elements_at_indices('string of text', (2, 3, 10, 12))
      ('r', 'i', 't', 'x')

   Return newly constructed tuple of references to `sequence` elements.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_elements_at_indices( )`` to
      ``seqtools.get_sequence_elements_at_indices( )``.
   '''

   result = [ ]
   for i, element in enumerate(sequence):
      if i in indices:
         result.append(element)
   return tuple(result)
