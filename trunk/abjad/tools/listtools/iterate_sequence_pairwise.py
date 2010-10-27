def iterate_sequence_pairwise(iter, mode = None):
   '''Yield adjacent element pairs in `iter`.

   Options for `mode`:

   * ``None``: return ``len(iter) - 1`` pairs from `iter` only.
   * ``'wrap'``: include ``(iter[-1], iter[0])`` at end.
   * ``'cycle'``: return indefinitely with no stop iteration.
   * ``int``: return exactly ``int`` pairs from `iter`.

   ::

      abjad> list(listtools.iterate_sequence_pairwise(range(6)))
      [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

   ::

      abjad> list(listtools.iterate_sequence_pairwise(range(6), 'wrap'))
      [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]

   ::

      abjad> list(listtools.iterate_sequence_pairwise(range(6), 9))
      [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 1), (1, 2), (2, 3)]

   .. versionchanged:: 1.1.2
      renamed ``listtools.pairwise( )`` to
      ``listtools.iterate_sequence_pairwise( )``.
   '''

   if mode is None:
      #for i in range(len(iter) - 1):
      #   yield (iter[i], iter[i + 1])
      prev = None
      for x in iter:
         cur = x
         if prev is not None:
            yield prev, cur
         prev = cur
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
