def is_increasing_monotonically(l):
   r'''.. versionadded:: 1.1.2

   True when the elements in `l` increase monotonically. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.is_increasing_monotonically(l)
      True

   ::

      abjad> l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
      abjad> listtools.is_increasing_monotonically(l)
      True

   ::
   
      abjad> l = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
      abjad> listtools.is_increasing_monotonically(l)
      True

   False when the elements in `l` do not increase monotonically. ::

      abjad> l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      abjad> listtools.is_increasing_monotonically(l)
      False

   ::

      abjad> l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
      abjad> listtools.is_increasing_monotonically(l)
      False

   True by definition when `l` is empty. ::

      abjad> l = [ ]
      abjad> listtools.is_increasing_monotonically(l)
      True
   '''

   prev = None
   for cur in l:
      if prev is not None:
         if not prev <= cur:
            return False
      prev = cur

   return True
