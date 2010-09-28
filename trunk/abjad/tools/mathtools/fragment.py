from abjad.core import Fraction


def fragment(n, cell):
   '''Fragment scalar *n* into *cell* fragments
   such that ``sum(cell) <= n``.

   ::

      abjad> mathtools.fragment(1, [Fraction(1, 2), Fraction(1, 4)])
      [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]

   ::

      abjad> mathtools.fragment(Fraction(1,2), [Fraction(1, 6), Fraction(1, 10)])
      [Fraction(1, 6), Fraction(1, 10), Fraction(7, 30)]

   Raise :exc:`TypeError` on nonnumeric *n*::

      abjad> mathtools.fragment('foo', [Fraction(1, 2), Fraction(1, 4)])
      TypeError

   Raise :exc:`ValueError` when ``sum(cell)`` is not 
   less than or equal to *n*::

      abjad> mathtools.fragment(1, [Fraction(3, 4), Fraction(3, 4)]) 
      ValueError

   .. todo:: Generalize and rename this function.
   '''

   if not isinstance(n, (int, float, long, Fraction)):
      raise TypeError

   if not sum(cell) <= n:
      raise ValueError

   residue = n - sum(cell)
   if 0 < residue:
      cell += [residue]

   return cell
