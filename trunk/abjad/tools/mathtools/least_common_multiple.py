from abjad.tools.mathtools.factors import factors


def least_common_multiple(*positive_integers):
   '''Return the least common multiple of `positive_integers`.

   ::

      abjad> mathtools.least_common_multiple(4, 5)
      20

   Works with more than two positive integers. ::

      abjad> mathtools.least_common_multiple(2, 4, 5, 10, 20)
      20

   .. todo:: Optimize.
   '''

   if len(positive_integers) == 1:
      if not isinstance(positive_integers[0], int):
         raise TypeError('must be integer.')
      if not 0 < positive_integers[0]:
         raise ValueError('must be positive.')
      return positive_integers[0]

   cur_lcm = _least_common_multiple(*positive_integers[:2])
   for remaining_positive_integer in positive_integers[2:]:
      cur_lcm = _least_common_multiple(cur_lcm, remaining_positive_integer)
   return cur_lcm


def _least_common_multiple(m, n):
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
