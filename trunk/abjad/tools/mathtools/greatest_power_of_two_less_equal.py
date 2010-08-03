from abjad.Rational import Rational
import math


def greatest_power_of_two_less_equal(n, i = 0):
   r'''Return greatest integer power of two 
   less than or equal to positive *n*.

   ::

      abjad> for n in range(10, 20):
      ...     print '\t%s\t%s' % (n, mathtools.greatest_power_of_two_less_equal(n))
      ... 
         10 8
         11 8
         12 8
         13 8
         14 8
         15 8
         16 16
         17 16
         18 16
         19 16

   When ``i = 1``, return the next-to-greatest integer power of ``2``
   less than or equal to *n*.

   ::

      abjad> for n in range(10, 20):
      ...     print '\t%s\t%s' % (n, mathtools.greatest_power_of_two_less_equal(n, i = 1))
      ... 
         10 4
         11 4
         12 4
         13 4
         14 4
         15 4
         16 8
         17 8
         18 8
         19 8

   When ``i = 2``, return the next-to-next-to-greatest integer power of ``2``
   less than or equal to *n*, and so on.

   Raise :exc:`TypeError` on nonnumeric *n*::

      abjad> mathtools.greatest_power_of_two_less_equal('foo')
      TypeError

   Raise :exc:`ValueError` on nonpositive *n*::

      abjad> mathtools.greatest_power_of_two_less_equal(-1)
      ValueError
   '''

   if not isinstance(n, (int, long, float, Rational)):
      raise TypeError

   if n <= 0:
      raise ValueError

   return 2 ** (int(math.log(n, 2)) - i)
