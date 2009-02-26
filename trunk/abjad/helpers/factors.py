def _factors(n):
   '''Returns all factors of n.'''

   assert isinstance(n, int)
   #assert n > 1
   assert n > 0

   d = 2
   factors = [1]
   while n > 1:
      if n % d == 0:
         factors.append(d)
         n = n/d
      else:
         d = d + 1
   return factors

