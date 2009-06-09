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

   Raise :exc:`TypeError` on noninteger *n*::

      abjad> mathtools.integer_halve('foo')
      TypeError

   Raise :exc:`ValueError` on nonpositive *n*::

      abjad> mathtools.integer_halve(-1)
      ValueError
''' 

   if not isinstance(n, (int, long)):
      raise TypeError

   if n <= 0:
      raise ValueError

   smaller_half = int(math.floor(n / 2))
   bigger_half = n - smaller_half

   if (smaller_half == bigger_half) and (even != 'allowed'):
      smaller_half -= 1
      bigger_half += 1

   if bigger == 'left':
      return (bigger_half, smaller_half)
   else:
      return (smaller_half, bigger_half)
