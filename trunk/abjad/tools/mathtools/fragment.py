
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

