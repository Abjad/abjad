def truncate_sequence_to_sum(l, total):
   '''Truncate list *l* such that ``sum(l) == total``.

   ::

      abjad> for n in range(10):
      ...     print n, seqtools.truncate_sequence_to_sum([2, 2, 2], n)
      ... 
      0 [ ]
      1 [1]
      2 [2]
      3 [2, 1]
      4 [2, 2]
      5 [2, 2, 1]
      6 [2, 2, 2]
      7 [2, 2, 2]
      8 [2, 2, 2]
      9 [2, 2, 2]
   
   ::

      abjad> l = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      abjad> for n in range(10):
      ...     print n, seqtools.truncate_sequence_to_sum(l, n)
      ... 
      0 [ ]
      1 [-1, 2]
      2 [-1, 2, -3, 4]
      3 [-1, 2, -3, 4, -5, 6]
      4 [-1, 2, -3, 4, -5, 6, -7, 8]
      5 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      6 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      7 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      8 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]
      9 [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

   Return empty list when ``total == 0``::

      abjad> seqtools.truncate_sequence_to_sum([1, 2, 3, 4, 5], 0)
      [ ]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> seqtools.truncate_sequence_to_sum('foo', 4)
      TypeError

   Raise :exc:`ValueError` on negative *total*::

      abjad> seqtools.truncate_sequence_to_sum([2, 2, 2], -4)
      ValueError

   .. versionchanged:: 1.1.2
      renamed ``seqtools.truncate_to_sum( )`` to
      ``seqtools.truncate_sequence_to_sum( )``.
   '''

   if not isinstance(l, list):
      raise TypeError

   if total < 0:
      raise ValueError

   #assert 0 <= total
   result = [ ]

   if total == 0:
      return result

   #kind = type(l)
   accumulation = 0
   for e in l:
      accumulation += e
      if accumulation < total:
         result.append(e)
      else:
         result.append(total - sum(result))
         break
   #return kind(result)
   return result
