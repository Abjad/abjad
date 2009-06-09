import math


def integer_halve(n, bigger = 'left', even = 'allowed'):
   '''Write positive integer *n* as the pair ``t = (left, right)`` 
   such that ``n == left + right``.

   When *n* is odd the greater part of ``t`` corresponds
   to the value of *bigger*::

      abjad> integer_halve(7, bigger = 'left')
      (4, 3)
      abjad> integer_halve(7, bigger = 'right')
      (3, 4)

   Likewise when *n* is even and ``even = 'disallowed'``::

      abjad> integer_halve(8, bigger = 'left', even = 'disallowed')
      (5, 3)
      abjad> integer_halve(8, bigger = 'right', even = 'disallowed')
      (3, 5)

   But when *n* is even and ``even = 'allowed'`` then ``left == right``
   and *bigger* is ignored::

      abjad> integer_halve(8)    
      (4, 4)
      abjad> integer_halve(8, bigger = 'left')
      (4, 4)
      abjad> integer_halve(8, bigger = 'right')
      (4, 4)
''' 

   smallerHalf = int(math.floor(n / 2))
   biggerHalf = n - smallerHalf

   if (smallerHalf == biggerHalf) and (even != 'allowed'):
      smallerHalf -= 1
      biggerHalf += 1

   if bigger == 'left':
      return (biggerHalf, smallerHalf)
   else:
      return (smallerHalf, biggerHalf)
