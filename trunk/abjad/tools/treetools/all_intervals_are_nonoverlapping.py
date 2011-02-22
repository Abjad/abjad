from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def all_intervals_are_nonoverlapping(intervals):
   '''True when all intervals in `intervals` in tree are non-overlapping.'''

   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)

   for i in range(1, len(tree.intervals)):
      if tree.inorder[i].low < tree.inorder[i -1].high:
         return False

   return True
