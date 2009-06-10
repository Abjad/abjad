def cumulative_products(l):
   '''Return a list of the cumulative products of the elements in *l*.

   ::

      abjad> mathtools.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
      [1, 2, 6, 24, 120, 720, 5040, 40320]

   ::
   
      abjad> mathtools.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
      [1, -2, -6, 24, 120, -720, -5040, 40320]

   Raise :exc:`TypeError` when *l* is neither list nor tuple::

      abjad> mathtools.cumulativ_products('foo')
      TypeError

   Raise :exc:`ValueError` when *l* is empty::

      abjad> mathtools.cumulative_products([ ])
      ValueError'''

   if not isinstance(l, (list, tuple)):
      raise TypeError

   if len(l) == 0:
      raise ValueError

   result = [l[0]]
   for element in l[1:]:
      result.append(result[-1] * element) 

   return result
