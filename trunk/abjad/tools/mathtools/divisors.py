import math


def divisors(n):
   '''Integer divisors of positive integer `n` in increasing order::

      abjad> mathtools.divisors(84)
      [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84

   ::

      abjad> for x in range(10, 20):
      ...     print x, mathtools.divisors(x)
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
      19 [1, 19]

   Raise type error on noninteger `n`.

   Raise value error on nonpositive `n`.

   Return list of one or more positive integers.
   '''

   if not isinstance(n, (int, long)):
      raise TypeError('"%s" must be integer.' % str(n))

   if n <= 0:
      raise ValueError('"%s" must be positive.' % str(n))
   
   ## Find all divisors from 1 to sqrt(n)
   divisors = [1]
   for i in range(2, int(math.sqrt(n)) + 1):
      if n % i == 0:
         divisors.append(i)
   
   codivisors = [n / i for i in reversed(divisors)]
   ## If the number is a perfect square
   ## we dont want the sqrt in the list twice
   if divisors[-1] == codivisors[0]:
      divisors.pop( )
      
   divisors.extend(codivisors)
 
   return divisors
