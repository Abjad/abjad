from fractions import Fraction


def arithmetic_mean(l):
   '''.. versionadded:: 1.1.1

   Return the arithmetic mean of the elements in iterable `l`.

   Where possible return an exact integer. ::

      abjad> l = [1, 2, 2, 20, 30]
      abjad> mathtools.arithmetic_mean(l)
      11

   Or return a rational. ::

      abjad> l = [1, 2, 20]
      abjad> mathtools.arithmetic_mean(l)
      Fraction(23, 3)

   Or return a float. ::

      abjad> l = [2, 2, 20.0]
      abjad> mathtools.arithmetic_mean(l)
      8.0

   .. versionchanged:: 1.1.2
      renamed ``seqtools.arithmetic_mean( )`` to
      ``mathtools.arithmetic_mean( )``.
   '''

   sum_l = sum(l)
   len_l = len(l)

   if isinstance(sum_l, float):
      return sum_l / len_l

   result = Fraction(sum(l), len(l))

   int_result = int(result)
   if int_result == result:
      return int_result
   else:
      return result
