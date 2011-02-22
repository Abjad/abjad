from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.shift_tree_to_offset import shift_tree_to_offset


def concatenate_trees(trees, padding = 0):
   '''Merge all trees in `trees`, offsetting each subsequent tree
   to start after the previous.'''

   assert all([isinstance(tree, IntervalTree) for tree in trees])
   assert isinstance(padding, (int, Fraction))
   assert 0 <= padding

   output_tree = IntervalTree(shift_tree_to_offset(trees[0], 0))
   for tree in trees[1:]:
      output_tree = IntervalTree([
         output_tree,
         shift_tree_to_offset(tree, output_tree.high_max + padding)
      ])    

   return output_tree
