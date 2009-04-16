def rotate(l, direction, n = 1, action = 'new'):
   '''>>> l = range(10)
      >>> listtools.rotate(l, 'left', 3)
      [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

      >>> listtools.rotate(l, 'right', 4)
      [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

      >>> listtools.rotate(l, 'left', 3, action = 'in place')
      >>> l
      [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]'''

   if direction == 'left':
      result = l[n:] + l[:n]
   elif direction == 'right':
      result = l[-n:] + l[:-n]
   else:
      raise ValueError("direction must be 'left' or 'right'.")

   if action == 'new':
      return result
   elif action == 'in place':
      l[:] = result
   else:
      raise ValueError("action must be 'new' or 'in place'.")
