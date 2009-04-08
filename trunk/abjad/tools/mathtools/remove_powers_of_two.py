def remove_powers_of_two(n):
   '''Remove powers of two from integer n.'''

   assert isinstance(n, int)
   while n % 2 == 0:
      n /= 2
   return n
