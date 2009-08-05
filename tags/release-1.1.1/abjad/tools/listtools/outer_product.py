def outer_product(lists):
   '''Return outer product of lists in ``lists``.

   ::

      abjad> listtools.outer_product([[1, 2, 3], ['a', 'b']])
      [[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b'], [3, 'a'], [3, 'b']]

   ::

      abjad> listtools.outer_product([[1, 2, 3], ['a', 'b'], ['X', 'Y']])
      [[1, 'a', 'X'], [1, 'a', 'Y'], [1, 'b', 'X'], [1, 'b', 'Y'], 
      [2, 'a', 'X'], [2, 'a', 'Y'], [2, 'b', 'X'], [2, 'b', 'Y'], 
      [3, 'a', 'X'], [3, 'a', 'Y'], [3, 'b', 'X'], [3, 'b', 'Y']]

   ::

      abjad> listtools.outer_product([[1, 2, 3], [4, 5], [6, 7, 8]])
      [[1, 4, 6], [1, 4, 7], [1, 4, 8], [1, 5, 6], [1, 5, 7], [1, 5, 8], 
      [2, 4, 6], [2, 4, 7], [2, 4, 8], [2, 5, 6], [2, 5, 7], [2, 5, 8], 
      [3, 4, 6], [3, 4, 7], [3, 4, 8], [3, 5, 6], [3, 5, 7], [3, 5, 8]]'''

   def helper(list1, list2):
      result = [ ]
      for l1 in list1:
         for l2 in list2:
            result.extend([l1 + [l2]])
      return result

   lists[0] = [[x] for x in lists[0]]
   result = reduce(helper, lists)

   return result
