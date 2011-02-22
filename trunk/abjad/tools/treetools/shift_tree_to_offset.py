from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree


def shift_tree_to_offset(tree, offset):
   '''Shift the start offset of all intervals in `tree` such that
   `tree.low` is equal to `offset`.'''

   assert isinstance(tree, IntervalTree)
   assert isinstance(offset, (int, Fraction))

   if tree.low_min == offset:
      return tree
   else:
      shift = offset - tree.low_min
      return IntervalTree([interval.shift_by_offset(offset) \
                           for interval in tree])
