def get_elements_at_indices(iterable, indices):
   '''.. versionadded:: 1.1.2

   Yield elements at `indices` in `iterable`::

      abjad> iterable = 'string of text'
      abjad> list(seqtools.get_elements_at_indices(iterable, (2, 3, 10, 12))) 
      ['r', 'i', 't', 'x']
   '''

   for i, element in enumerate(iterable):
      if i in indices:
         yield element
