from abjad.Rational import Rational


def truncate_subruns(l):
   '''Truncate subruns of like elements in *l* to length ``1``::

      abjad> l = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
      abjad> listtools.truncate_subruns(l)
      [1, 2, 3, 9, 4]

   Return empty list when *l* is empty::

      abjad> listtools.truncate_subruns([ ])
      []

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> listtools.truncate_subruns(1)
      TypeError
   '''

   if not isinstance(l, list):
      raise TypeError

   assert all([isinstance(x, (int, float, Rational)) for x in l])

   result = [ ]

   if l:
      result.append(l[0])
      for element in l[1:]:
         if not element == result[-1]:
            result.append(element)

   return result
