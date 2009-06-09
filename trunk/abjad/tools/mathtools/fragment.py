from abjad.rational.rational import Rational


def fragment(n, cell):
   '''Fragment scalar *n* into *cell* fragments
   such that ``sum(cell) <= n``.

   ::

      abjad> mathtools.fragment(1, [Rational(1, 2), Rational(1, 4)])
      [Rational(1, 2), Rational(1, 4), Rational(1, 4)]

   ::

      abjad> mathtools.fragment(Rational(1,2), [Rational(1, 6), Rational(1, 10)])
      [Rational(1, 6), Rational(1, 10), Rational(7, 30)]

   Raise :exc:`TypeError` on nonnumeric *n*::

      abjad> mathtools.fragment('foo', [Rational(1, 2), Rational(1, 4)])
      TypeError

   Raise :exc:`ValueError` when ``sum(cell)`` is not 
   less than or equal to *n*::

      abjad> mathtools.fragment(1, [Rational(3, 4), Rational(3, 4)]) 
      ValueError'''

   if not isinstance(n, (int, float, long, Rational)):
      raise TypeError

   if not sum(cell) <= n:
      raise ValueError

   residue = n - sum(cell)
   if 0 < residue:
      cell += [residue]

   return cell
