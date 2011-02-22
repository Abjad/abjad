from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree


def shift_tree_by_offset(tree, offset):
   '''Shift the start offset of all intervals in `tree` by `offset`.'''

   assert isinstance(tree, IntervalTree)
   assert isinstance(offset, (int, Fraction))

   if offset == 0:
      return tree
   else:
      return IntervalTree([interval.shift_by_offset(offset) \
                           for interval in tree])
