from factors import factors


def least_common_multiple(m, n):
   '''Return the least common multiple of integers `m` and `n`.

   ::

      abjad> mathtools.least_common_multiple(4, 5)
      20

   ::

      abjad> mathtools.least_common_multiple(4, 6)
      12

   .. todo:: Optimize.
   '''

   ## check input
   if not isinstance(m, int):
      raise TypeError

   if not isinstance(n, int):
      raise TypeError

   ## find factors of m and n
   factors_m = factors(m)
   factors_n = factors(n)

   ## remove duplicated shared factors
   for x in factors_m:
      try:
         factors_n.remove(x)
      except ValueError:
         pass

   ## calculate product of shared factors
   result = 1
   for x in factors_m + factors_n:
      result *= x

   ## return product
   return result
