from abjad.tools.mathtools.divisors import divisors


def greatest_common_divisor(*integers):
   '''.. versionadded:: 1.1.2

   Greatest common divisor of one or more positive `integers`::

      abjad> mathtools.greatest_common_divisor(84, 94, 144)
      2

   Return positive integer.

   Raise type error on noninteger `integers`.

   Raise value error on nonpositive `integers`.
   '''
      
   common_divisors = None
   for positive_integer in integers:
      if not isinstance(positive_integer, int):
         raise TypeError('must be integer.')
      if not 0 < positive_integer:
         raise ValueError('must be positive.')
      all_divisors = set(divisors(positive_integer))
      if common_divisors is None:
         common_divisors = all_divisors
      else:
         common_divisors &= all_divisors
         if common_divisors == set([1]):
            return 1
   return max(common_divisors)
