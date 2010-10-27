def remove_duplicates_from_sequence(l):
   '''Return a newly constructed list of the unique 
   elements in iterable `l`. ::

      abjad> l = [1, 1, 1, 2, 3, 3, 4, 5]
      abjad> seqtools.remove_duplicates_from_sequence(l)
      [1, 2, 3, 4, 5]

   Defined equal to ``list(set(l))``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.unique( )`` to
      ``seqtools.remove_duplicates_from_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.remove_duplicates_from_iterable( )`` to
      ``seqtools.remove_duplicates_from_sequence( )``.
   '''

   return list(set(l))
