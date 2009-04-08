def is_divisor_of(m, n):
   '''True if m is an integer divisor of n, otherwise False.'''

   assert isinstance(m, int)
   assert isinstance(n, int)

   return n % m == 0
