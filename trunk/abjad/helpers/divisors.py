def _divisors(n):
   '''Return a Python list of the integer divisors of n in increasing order.

      >>> for x in range(10, 20):
      ...     print x, _divisors(x)
      ... 
      10 [1, 2, 5, 10]
      11 [1, 11]
      12 [1, 2, 3, 4, 6, 12]
      13 [1, 13]
      14 [1, 2, 7, 14]
      15 [1, 3, 5, 15]
      16 [1, 2, 4, 8, 16]
      17 [1, 17]
      18 [1, 2, 3, 6, 9, 18]
      19 [1, 19]'''

   assert isinstance(n, int)
   
   result = [ ]
   for i in range(1, n + 1):
      quotient = float(n) / i
      if quotient == int(quotient):
         result.append(i)

   return result
