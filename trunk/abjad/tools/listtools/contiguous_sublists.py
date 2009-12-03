def contiguous_sublists(l, min_length = 0, max_length = None):
   '''.. versionadded:: 1.1.2

   Yield all left-to-right contiguous sublists in l
   of minimum length at least `min_length` and maximum length
   at most `max_length`. ::

      abjad> l = range(10)
      abjad> for sublist in listtools.contiguous_sublists(l, 4, 5):
      ...     sublist
      ... 
      [0, 1, 2, 3]
      [0, 1, 2, 3, 4]
      [1, 2, 3, 4]
      [1, 2, 3, 4, 5]
      [2, 3, 4, 5]
      [2, 3, 4, 5, 6]
      [3, 4, 5, 6]
      [3, 4, 5, 6, 7]
      [4, 5, 6, 7]
      [4, 5, 6, 7, 8]
      [5, 6, 7, 8]
      [5, 6, 7, 8, 9]
      [6, 7, 8, 9]
   '''

   len_l = len(l)

   if max_length is None:
      max_length = len_l

   for i in range(len_l):
      for j in range(i + min_length, i + max_length + 1):
         if j <= len_l:
            sublist = l[i:j]
            yield sublist
