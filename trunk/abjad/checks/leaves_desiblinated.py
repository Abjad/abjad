from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


# TODO - make this work in cases where expr contains one or more parallel
# containers;
# test case:
# t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
# t = Staff(t * 2)
# t = Score(t * 2)
# check_next_leaves(t) should work fine and not complain at note 5

class LeavesDesiblinated(_Check):

   def _run(self, expr):
      from abjad.leaf.leaf import _Leaf
      violators = [ ]
      leaves = list(iterate(expr, _Leaf))
      total, bad = 0, 0
      if leaves:
         leaves.pop( )
         total += 1
         for l in leaves:
            if not l.next:
               violators.append(l)
               bad += 1
            total += 1
      return violators, total
