def remove_duplicates_from_sequence(sequence):
   '''Remove duplicates from `sequence`::

      abjad> seqtools.remove_duplicates_from_sequence([1, 1, 1, 2, 3, 3, 4, 5])
      [1, 2, 3, 4, 5]

   Defined equal to ``list(set(sequence))``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.unique( )`` to
      ``seqtools.remove_duplicates_from_sequence( )``.
   '''

   return list(set(sequence))
