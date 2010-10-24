def permute_iterable(iterable, ordering):
   '''.. versionadded:: 1.1.2

   Return `iterable` permuted by `ordering`. ::

      abjad> listtools.permute_iterable([10, 11, 12, 13, 14, 15], [5, 4, 0, 1, 2, 3])
      (15, 14, 10, 11, 12, 13)

   .. versionchanged:: 1.1.2
      renamed ``listtools.permute( )`` to
      ``listtools.permute_iterable( )``.
   '''

   list_iterable = list(iterable)
   if not len(list_iterable) == len(ordering):
      raise ValueError('ordering must be %s elements in length.' %
         len(list_iterable))
   if not list(sorted(ordering)) == range(len(ordering)):
      raise ValueError('ordering must contain elements 0, ..., %s exactly.' %
         len(list_iterable))
   

   permutation = [ ]
   for index in ordering:
      permutation.append(list_iterable[index])
   return tuple(permutation)
