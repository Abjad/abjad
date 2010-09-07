import math


def binomial_coefficient(n, k):
   r'''.. versionadded:: 1.1.2

   Return the binomial coefficient of `n` choose `k`:

      abjad> for x in range(8):
      ...     print x, '\t', mathtools.binomial_coefficient(8, x)
      ... 
      0  1
      1  8
      2  28
      3  56
      4  70
      5  56
      6  28
      7  8
   '''

   return math.factorial(n) / (math.factorial(n - k) * math.factorial(k))
