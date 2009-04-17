def increase_cyclic(l, s, shield = True, trim = True, action = 'in place'):
   '''Cyclically increase elements of l by the elements of s;
      map nonpositive values to 1 by default.

      >>> l = range(10)
      >>> increase_cyclic(l, [2, 0])
      >>> l
      [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

      >>> l = range(10)
      >>> increase_cyclic(l, [10, -10])
      >>> l
      [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]

      >>> l = range(10)
      >>> increase_cyclic(l, [10, -10], shield = False)
      >>> l
      [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]'''

   result = [ ]

   for i, element in enumerate(l):
      new = element + s[i % len(s)]
      if shield and new <= 0:
         new = 1
      result.append(new)

   if action == 'in place':
      l[:] = result
   else:
      return result
