def retain_elements_at_indices(sequence, indices):
   '''.. versionadded:: 1.1.2

   Retain `sequence` elements at `indices`::

      abjad> seqtools.retain_elements_at_indices(range(20), [1, 16, 17, 18])
      [1, 16, 17, 18]

   Ignore negative indices.

   Return list.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if i in indices:
         #yield element
         result.append(element)

   return result
