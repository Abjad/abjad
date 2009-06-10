def cumulative_sums(l):
   '''Return a list of the cumulative sums of the elements in *l*.

   ::

      abjad> mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8])
      [1, 3, 6, 10, 15, 21, 28, 36]

   ::
   
      abjad> mathtools.cumulative_sums([1, -2, 3, -4, 5, -6, 7, -8])
      [1, -1, 2, -2, 3, -3, 4, -4]

   Raise :exc:`TypeError` when *l* is neither list nor tuple::

      abjad> mathtools.cumulative_sums('foo')
      TypeError

   Raise :exc:`ValueError` when *l* is empty::

      abjad> mathtools.cumulative_sums([ ])
      ValueError'''


   if not isinstance(l, (list, tuple)):
      raise TypeError

   if len(l) == 0:
      raise ValueError

   result = [l[0]]
   for element in l[1:]:
      result.append(result[-1] + element) 

   return result
