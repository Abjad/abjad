from abjad.rational import Rational


def is_numeric(l):
   '''.. versionadded:: 1.1.1

   Return ``True`` when all elements in iterable `l` are numeric,
   otherwise ``False``. ::

      abjad> listtools.is_numeric([1, 2, 4.5, 5.5, Rational(13, 8)])
      True

   Defined equal to ``all([isinstance(x, (int, long, float, Rational)) 
   for x in l])``.

   .. note:: implementation will probably change under Python 2.6.
   '''

   return all([isinstance(x, (int, long, float, Rational)) for x in l])
