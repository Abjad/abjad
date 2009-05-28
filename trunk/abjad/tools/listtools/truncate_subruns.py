from abjad.rational.rational import Rational


def truncate_subruns(l):
   '''Truncate subruns in ``l`` to length ``1``.

   Example::

      abjad> l = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
      abjad> listtools.truncate_subruns(l)
      [1, 2, 3, 9, 4]'''

   assert isinstance(l, list)
   assert all([isinstance(x, (int, float, Rational)) for x in l])

   result = [ ]

   if l:
      result.append(l[0])
      for element in l[1:]:
         if not element ==result[-1]:
            result.append(element)

   return result
