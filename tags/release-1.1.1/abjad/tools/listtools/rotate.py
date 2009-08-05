def rotate(l, n):
   '''When *n* is positive, rotate the elements in *l* *n* places
   to the right. When *n* is negative, rotate the elements in *l*
   *n* places to the left.
   
   ::

      abjad> l = range(10)
      abjad> listtools.rotate(l, -3)
      [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   ::

      abjad> listtools.rotate(l, 4)
      [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]'''

   return l[-n:] + l[:-n]
