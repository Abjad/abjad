def sign(l):
   '''Return ``1`` when all elements in *l* are positive. ::

      abjad> listtools.sign([1, 2, 3])
      1
   
   Return ``-1`` when all elements in *l* are negative. ::

      abjad> listtools.sign([-1, -2, -3])
      -1

   Return ``0`` when *l* is empty. ::

      abjad> listtools.sign([ ])
      0

   Otherwise, return ``None``. ::

      abjad> listtools.sign([1, 2, -3]) is None
      True
   '''

   if len(l) == 0:
      return 0
   elif all([0 < x for x in l]):
      return 1
   elif all([x < 0 for x in l]):
      return -1
   else:
      return None
