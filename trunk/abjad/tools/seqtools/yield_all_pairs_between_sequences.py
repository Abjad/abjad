def yield_all_pairs_between_sequences(l, m):
   '''.. versionadded:: 1.1.2

   Yield pairs from `l` to `m`. ::

      abjad> for pair in seqtools.yield_all_pairs_between_sequences([1, 2, 3], [4, 5]):
      ...     pair 
      ... 
      (1, 4)
      (1, 5)
      (2, 4)
      (2, 5)
      (3, 4)
      (3, 5)

   .. versionchanged:: 1.1.2
      renamed ``seqtools.pairs_from_to( )`` to
      ``seqtools.yield_all_pairs_between_sequences( )``.
   '''

   for x in l:
      for y in m:
         yield x, y
