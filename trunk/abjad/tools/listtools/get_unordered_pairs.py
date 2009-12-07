def get_unordered_pairs(l):
   '''Return ordered list of unordered pairs in `l`.
   
   ::
   
      abjad> listtools.get_unordered_pairs([1, 2, 3, 4])
      [set([1, 2]), set([1, 3]), set([1, 4]), set([2, 3]), set([2, 4]), set([3, 4])]

   ::

      abjad> listtools.get_unordered_pairs([1, 2])
      [set([1, 2])]

   ::

      abjad> listtools.get_unordered_pairs([1])
      []

   ::

      abjad> listtools.get_unordered_pairs([ ])
      []
      
   .. note:: This function returns a list instead of a generator.
   '''

   result = [ ]
   l_copy = list(l)

   for i, x in enumerate(l):
      for y in l_copy[i+1:]:
         result.append(set([x, y]))

   return result
