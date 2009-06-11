def true_indices(l):
   '''Return the nonnegative integers ``i, j, ...``
   for which ``l[i], l[j], ...`` are ``True``.

   ::

      abjad> l = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
      abjad> listtools.true_indices(l)
      [3, 4, 5, 9, 10, 11]

   ::

      abjad> l = [0, 0, 0, 0, 0, 0]
      abjad> listtools.true_indices(l)
      []

   Raise :exc:`TypeError` when *l* is neither list nor tuple::

      abjad> listtools.true_indices('foo')
      TypeError
   '''

   if not isinstance(l, (list, tuple)):
      raise TypeError

   result = [ ]

   for i, x in enumerate(l):
      if bool(x):
         result.append(i)

   return result
