def get_unordered_pairs(l):
   '''Return list of unordered pairs in `l`.
   
   ::
   
      abjad> listtools.get_unordered_pairs([1, 2, 3, 4])
      [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


   ::

      abjad> listtools.get_unordered_pairs([1, 2])
      [set([1, 2])]

   ::

      abjad> listtools.get_unordered_pairs([1])
      []

   ::

      abjad> listtools.get_unordered_pairs([ ])
      []

   ::

      abjad> listtools.get_unordered_pairs([1, 1, 1])
      [(1, 1), (1, 1), (1, 1)]

   ::

      abjad> listtools.get_unordered_pairs(set([1, 2, 3]))
      [(1, 2), (1, 3), (2, 3)]

   .. note:: pairs are tuples instead of sets to accommodate 
      duplicate value input in `l`.

   .. todo:: make ``listtools.get_unordered_pairs( )`` return
      a list of two-element multisets.
   '''

   result = [ ]
   l_copy = list(l)

   for i, x in enumerate(l_copy):
      for y in l_copy[i+1:]:
         pair = (x, y)
         result.append(pair)

   return result
