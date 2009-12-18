import math


def is_dotted_integer(n):
   '''.. versionadded:: 1.1.2

   True when the absolute value of `n` is of the form 
   ``2 ** k - 1`` for integer ``2 < k``. ::
       
      abjad> for n in range(16):
      ...     print '%s\t%s' % (n, mathtools.is_dotted_integer(n))
      ... 
      0       False
      1       False
      2       False
      3       True
      4       False
      5       False
      6       False
      7       True
      8       False
      9       False
      10      False
      11      False
      12      False
      13      False
      14      False
      15      True
   '''

   x = math.log(abs(n) + 1, 2)
   return 1 < abs(n) and int(x) == x
