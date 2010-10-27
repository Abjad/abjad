def negate_elements_at_indices_absolutely(l, indices, period = None):
   '''Negate the absolute value of elements in ``l`` at ``indices``.
   When ``period`` is a positive integer, read ``indices`` 
   cyclically according to ``period``.

   ::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.negate_elements_at_indices(l, [0, 1, 2], period = None)
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   ::

      abjad> l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
      abjad> seqtools.negate_elements_at_indices(l, [0, 1, 2], period = 5)
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> seqtools.negate_elements_at_indices_absolutely('foo', [0, 1, 2])
      TypeError
   '''

   result = [ ]

   for i, element in enumerate(l):
      if (i in indices) or (period and i % period in indices):
         result.append(-abs(element))
      else:
         result.append(element)

   return result
