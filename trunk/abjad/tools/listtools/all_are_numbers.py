from fractions import Fraction


def all_are_numbers(l):
   '''.. versionadded:: 1.1.1

   Return ``True`` when all elements in iterable `l` are numeric,
   otherwise ``False``. ::

      abjad> listtools.all_are_numbers([1, 2, 4.5, 5.5, Fraction(13, 8)])
      True

   Defined equal to ``all([isinstance(x, (int, long, float, Fraction)) 
   for x in l])``.

   .. note:: implementation will probably change under Python 2.6.

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_numeric( )`` to
      ``listtools.all_are_numbers( )``.
   '''

   return all([isinstance(x, (int, long, float, Fraction)) for x in l])
