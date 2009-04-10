def factors(n):
   '''Returns all factors of n.'''

   assert isinstance(n, int)
   assert 0 < n

   d = 2
   factors = [1]
   while 1 < n:
      if n % d == 0:
         factors.append(d)
         n = n/d
      else:
         d = d + 1
   return factors


