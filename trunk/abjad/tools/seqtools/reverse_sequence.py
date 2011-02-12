def reverse_sequence(sequence):
   '''.. versionadded:: 1.1.2

   Reverse `sequence`::

      abjad> seqtools.reverse_sequence((1, 2, 3, 4, 5))
      (5, 4, 3, 2, 1)

   Return new `sequence` object.
   '''

   return type(sequence)(reversed(sequence))
