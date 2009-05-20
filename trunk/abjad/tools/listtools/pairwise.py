def pairwise(iter, mode = None):
   '''Iterate adjacent pairs of elements in 'iter'.

      Options for 'mode':

      * None: return len(iter) - 1 pairs from iter only.
      * 'wrap': include (iter[-1], iter[0]) at end.
      * 'cycle': return indefinitely with no StopIteration.
      * int: return exactly int pairs from iter.

      Example::

         abjad> list(listtools.pairwise(range(6)))
         [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

      Example::

         abjad> list(listtools.pairwise(range(6), 'wrap'))
         [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]

      Example::

         abjad> list(listtools.pairwise(range(6), 9))
         [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 1), (1, 2), (2, 3)]'''

   if mode is None:
      for i in range(len(iter) - 1):
         yield (iter[i], iter[i + 1])
   elif mode == 'wrap':
      for i in range(len(iter)):
         yield (iter[i], iter[(i + 1) % len(iter)])
   elif mode == 'cycle':
      i = 0
      while True:
         yield (iter[i % len(iter)], iter[(i + 1) % len(iter)])
         i += 1
   elif isinstance(mode, (int, long)):
      for i in range(mode):
         yield (iter[i % len(iter)], iter[(i + 1) % len(iter)])
   else:
      raise ValueError('unknown pairwise mode %s.' % mode)
