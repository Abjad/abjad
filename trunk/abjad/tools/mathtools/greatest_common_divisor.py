from abjad.tools.mathtools.divisors import divisors as mathtools_divisors


def greatest_common_divisor(*positive_integers):
   '''.. versionadded:: 1.1.2

   Return the greatest common divisor of one or more `positive_integers`. ::

      abjad> mathtools.greatest_common_divisor(84, 94, 144)
      2

   Raise TypeError on noninteger input. ::

      abjad> mathtools.greatest_common_divisor('foo')
      TypeError

   Raise ValueError on nonpositive input. ::

      abjad> mathtools.greatest_common_divisor(-99)
      ValueError
   '''
      
   common_divisors = None
   for positive_integer in positive_integers:
      if not isinstance(positive_integer, int):
         raise TypeError('must be integer.')
      if not 0 < positive_integer:
         raise ValueError('must be positive.')
      divisors = set(mathtools_divisors(positive_integer))
      if common_divisors is None:
         common_divisors = divisors
      else:
         common_divisors &= divisors
         if common_divisors == set([1]):
            return 1
   return max(common_divisors)
