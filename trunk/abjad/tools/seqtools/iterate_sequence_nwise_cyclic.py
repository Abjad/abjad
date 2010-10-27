def iterate_sequence_nwise_cyclic(iterable, n):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` cyclically `n` at a time. ::

      abjad> g = seqtools.iterate_sequence_nwise_cyclic(range(6), 3)
      abjad> for n in range(10):
      ...   print g.next( )
      (0, 1, 2)
      (1, 2, 3)
      (2, 3, 4)
      (3, 4, 5)
      (4, 5, 0)
      (5, 0, 1)
      (0, 1, 2)
      (1, 2, 3)
      (2, 3, 4)
      (3, 4, 5)

   .. versionchanged:: 1.1.2
      renamed ``seqtools.nwise_cyclic( )`` to
      ``seqtools.iterate_sequence_nwise_cyclic( )``.
   '''

   buffer = [ ]
   long_enough = False
   for element in iterable:
      buffer.append(element)
      if not long_enough:
         if n <= len(buffer):
            long_enough = True
      if long_enough:
         yield tuple(buffer[-n:])
   
   len_iterable = len(buffer)
   cur = len_iterable - n + 1
   while True:
      output = [ ]
      for local_offset in range(n):
         index = (cur + local_offset) % len_iterable
         output.append(buffer[index])
      yield tuple(output)
      cur += 1
      cur %= len_iterable
