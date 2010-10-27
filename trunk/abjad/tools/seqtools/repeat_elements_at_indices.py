def repeat_elements_at_indices(iterable, indices, total):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` at `indices` to `total` length. ::

      abjad> list(seqtools.repeat_elements_at_indices(range(10), [6, 7, 8], 3))
      [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]

   Function output is "structure-wrapped" to better allow additional
   transforms by other functions. Remove structure wrapping with flatten. ::

      abjad> t = list(seqtools.repeat_elements_at_indices(range(10), [6, 7, 8], 3))
      abjad> seqtools.flatten_sequence(t)
      [0, 1, 2, 3, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9]
   '''

   for i, element in enumerate(iterable):
      if i in indices:
         yield total * [element]
      else:
         yield element
