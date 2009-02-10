from abjad.helpers.tcopy import tcopy


def cyclic_extend(expr, n = 1, reps = 1):
   '''Copy the last n elements in expr;
      then extend expr with addendum reps times.'''

   # get start and stop indices
   stop = len(expr)
   start = stop - n

   # for every repetition
   for x in range(reps):

      # copy last n elements of expr
      addendum = tcopy(expr[start:stop])

      # extend expr with addendum
      expr.extend(addendum)
