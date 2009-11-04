from abjad.tools.mathtools.next_integer_partition import \
   next_integer_partition as mathtools_next_integer_partition


def integer_partitions(n):
   r'''.. versionadded:: 1.1.2

   Yield all integer partitions of positive integer `n` in
   descending lex order. ::

      abjad> for partition in mathtools.integer_partitions(7):
      ...     partition
      ... 
      (7,)
      (6, 1)
      (5, 2)
      (5, 1, 1)
      (4, 3)
      (4, 2, 1)
      (4, 1, 1, 1)
      (3, 3, 1)
      (3, 2, 2)
      (3, 2, 1, 1)
      (3, 1, 1, 1, 1)
      (2, 2, 2, 1)
      (2, 2, 1, 1, 1)
      (2, 1, 1, 1, 1, 1)
      (1, 1, 1, 1, 1, 1, 1)
   '''

   if not isinstance(n, int):
      raise TypeError('must be integer.')
   if not 0 < n:
      raise ValueError('must be positive.')

   partition = (n, )
   while partition is not None:
      yield partition
      partition = mathtools_next_integer_partition(partition)

   #raise StopIteration
