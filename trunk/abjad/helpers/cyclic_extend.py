from abjad.helpers.tcopy import tcopy


def cyclic_extend(expr, n = 1, total = 2):
   '''Copy the last n elements in expr;
      then extend expr with addendum to a total of total copies.'''

   # get start and stop indices
   stop = len(expr)
   start = stop - n

   # for the total number of elements less one
   for x in range(total - 1):

      # copy last n elements of expr
      addendum = tcopy(expr[start:stop])

      # extend expr with addendum
      expr.extend(addendum)

   return expr
