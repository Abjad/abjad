from __future__ import division
from abjad.rational.rational import Rational
from abjad.helpers.rationalize import rationalize

def fragment(total, cell):
   '''
   Fragment a given scalar value into cell fragments.
   sum(cell) must be <= total.

   Examples:
   >>> fragment(1, [Rational(1, 2), Rational(1, 4)])
   [Rational(1, 2), Rational(1, 4), Rational(1, 4)]

   >>> fragment(Rational(1,2), [Rational(1, 6), Rational(1, 10)])
   [Rational(1, 6), Rational(1, 10), Rational(7, 30)]

   '''
   assert sum(cell) <= total
   residue = total - sum(cell)
   if residue > 0:
      cell += [residue]
   return cell


def divide(total, parts):
   '''
   Divide a scalar total (int, float or rational) into the proportions given
   by the numbers in parts.
   Example:
   >>>  divide(Rational(1, 2), [1,1,3]) returns
   [Rational(1, 10), Rational(1, 10), Rational(3, 10)]
   '''
   return [total * p / sum(parts) for p in parts]


def truncate_to_sum(ls, total):
   '''
   Truncate the given numeric list ls so that sum(ls) == total.
   Example:
   >>> for i in range(7):
   ...    truncate_to_sum([2,2,2], i)
   [0]
   [1]
   [2]
   [2, 1]
   [2, 2]
   [2, 2, 1]
   [2, 2, 2]
   '''
   assert total >= 0
   result = [ ]
   kind = type(ls)
   accumulation = 0
   for e in ls:
      accumulation += e
      if accumulation < total:
         result.append(e)
      else:
         result.append(total - sum(result))
         break
   return kind(result)
      

