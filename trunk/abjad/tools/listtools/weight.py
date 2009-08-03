def weight(l):
   '''Return the sum of absolute value of elements in iterable `l`.

   ::

      abjad> l = [-1, -2, 3, 4, 5]
      abjad> listtools.weight(l)
      15
   '''

   return sum([abs(element) for element in l])
