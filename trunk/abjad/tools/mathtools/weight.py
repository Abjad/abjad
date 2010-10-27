def weight(l):
   '''Return the sum of absolute value of elements in iterable `l`.

   ::

      abjad> l = [-1, -2, 3, 4, 5]
      abjad> mathtools.weight(l)
      15

   .. versionchanged:: 1.1.2
      renamed ``seqtools.weight( )`` to
      ``mathtools.weight( )``.
   '''

   return sum([abs(element) for element in l])
