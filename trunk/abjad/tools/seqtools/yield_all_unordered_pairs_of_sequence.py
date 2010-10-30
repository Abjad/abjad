def yield_all_unordered_pairs_of_sequence(l):
   '''Return list of unordered pairs in `l`.
   
   ::
   
      abjad> seqtools.yield_all_unordered_pairs_of_sequence([1, 2, 3, 4])
      [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


   ::

      abjad> seqtools.yield_all_unordered_pairs_of_sequence([1, 2])
      [set([1, 2])]

   ::

      abjad> seqtools.yield_all_unordered_pairs_of_sequence([1])
      [ ]

   ::

      abjad> seqtools.yield_all_unordered_pairs_of_sequence([ ])
      [ ]

   ::

      abjad> seqtools.yield_all_unordered_pairs_of_sequence([1, 1, 1])
      [(1, 1), (1, 1), (1, 1)]

   ::

      abjad> seqtools.yield_all_unordered_pairs_of_sequence(set([1, 2, 3]))
      [(1, 2), (1, 3), (2, 3)]

   .. note:: pairs are tuples instead of sets to accommodate 
      duplicate value input in `l`.

   .. todo:: make ``seqtools.yield_all_unordered_pairs_of_sequence( )`` return
      a list of two-element multisets.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_unordered_pairs( )`` to
      ``seqtools.yield_all_unordered_pairs_of_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.yield_all_unordered_pairs_in_sequence( )`` to
      ``seqtools.yield_all_unordered_pairs_of_sequence( )``.
   '''

   result = [ ]
   l_copy = list(l)

   for i, x in enumerate(l_copy):
      for y in l_copy[i+1:]:
         pair = (x, y)
         result.append(pair)

   return result
