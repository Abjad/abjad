def pairwise(iter):
   '''Iterate len(iter) - 1 pairs from iter.

   >>> t = range(6)
   >>> pairs = pairwise(t)
   >>> t.next( )
   (0, 1)
   >>> t.next( )
   (1, 2)'''

   for i in range(len(iter) - 1):
      yield (iter[i], iter[i + 1])
