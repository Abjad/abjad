def get_elements_at_indices(sequence, indices):
   '''.. versionadded:: 1.1.2

   Get `sequence` elements at `indices`::

      abjad> list(seqtools.get_elements_at_indices('string of text', (2, 3, 10, 12))) 
      ['r', 'i', 't', 'x']

   Return generator of references to `sequence` elements.
   '''

   for i, element in enumerate(sequence):
      if i in indices:
         yield element
