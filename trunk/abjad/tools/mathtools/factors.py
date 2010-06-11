def factors(n):
   '''Return a list of all integer factors of posittive *n*::

      abjad> mathtools.factors(84)
      [1, 2, 2, 3, 7]

   ::

      abjad> for n in range(10, 20):
      ...   print n, mathtools.factors(n)
      ... 
      10 [1, 2, 5]
      11 [1, 11]
      12 [1, 2, 2, 3]
      13 [1, 13]
      14 [1, 2, 7]
      15 [1, 3, 5]
      16 [1, 2, 2, 2, 2]
      17 [1, 17]
      18 [1, 2, 3, 3]
      19 [1, 19]

   Raise :exc:`TypeError` on noninteger *n*::

      abjad> mathtools.factors(7.5)
      TypeError

   Raise :exc:`ValueError` on nonpositive integer *n*::

      abjad> mathtools.factors(-1)
      ValueError
   '''

   if not isinstance(n, (int, long)):
      raise TypeError

   if n <= 0:
      raise ValueError

   d = 2
   factors = [1]
   while 1 < n:
      if n % d == 0:
         factors.append(d)
         n = n/d
      else:
         d = d + 1
   return factors
