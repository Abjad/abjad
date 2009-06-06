def rotate(l, direction, n = 1):
   '''Rotate the elements of *l* *n* places to the *direction*.
   
   * *direction* must be either `'left'` or `'right'`.

   ::

      >>> l = range(10)
      >>> listtools.rotate(l, 'left', 3)
      [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   ::

      >>> listtools.rotate(l, 'right', 4)
      [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

   .. todo:: Eliminate *direction* in favor of signed *n*.'''

   if direction == 'left':
      result = l[n:] + l[:n]
   elif direction == 'right':
      result = l[-n:] + l[:-n]
   else:
      raise ValueError("direction must be 'left' or 'right'.")

   return result
