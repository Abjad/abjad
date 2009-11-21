from abjad.rational import Rational


def arithmetic_mean(l):
   '''.. versionadded:: 1.1.1

   Return the arithmetic mean of the elements in iterable `l`.

   Where possible return an exact integer. ::

      abjad> l = [1, 2, 2, 20, 30]
      abjad> listtools.arithmetic_mean(l)
      11

   Otherwise return a rational. ::

      abjad> l = [1, 2, 20]
      abjad> listtools.arithmetic_mean(l)
      Rational(23, 3)

   Never return a float.
   '''

   sum_l = sum(l)
   len_l = len(l)

   if isinstance(sum_l, float):
      return sum_l / len_l

   result = Rational(sum(l), len(l))

   int_result = int(result)
   if int_result == result:
      return int_result
   else:
      return result
