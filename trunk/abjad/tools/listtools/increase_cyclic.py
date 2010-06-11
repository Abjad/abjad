def increase_cyclic(l, s, shield = True, trim = True):
   '''Cyclically increase elements of *l* by the elements of *s*.
   Map nonpositive values to ``1`` by default.

   ::

      abjad> l = range(10)
      abjad> listtools.increase_cyclic(l, [2, 0])
      [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

   ::

      abjad> l = range(10)
      abjad> listtools.increase_cyclic(l, [10, -10])
      [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]

   ::

      abjad> l = range(10)
      abjad> listtools.increase_cyclic(l, [10, -10], shield = False)
      [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

   Raise :exc:`TypeError` when *l* is neither list nor tuple::

      abjad> listtools.increase_cyclic('foo', [10, -10])
      TypeError
   '''

   if not isinstance(l, (list, tuple)):
      raise TypeError

   result = [ ]

   for i, element in enumerate(l):
      new = element + s[i % len(s)]
      if shield and new <= 0:
         new = 1
      result.append(new)

   return result
