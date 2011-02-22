from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools import compute_depth_of_intervals


def explode_tree_compactly(tree):
   '''Explode the intervals in `tree` into n non-overlapping trees, 
   where n is the maximum depth of `tree`.

   Returns an array of `IntervalTree` instances.

   The algorithm will attempt to insert the exploded intervals
   into the lowest-indexed resultant tree with free space.
   '''
    
   assert isinstance(tree, IntervalTree)

   depth_tree = compute_depth_of_intervals(tree)
   max_depth = max([x.data['depth'] for x in depth_tree])
   layers = [[ ] for i in range(max_depth)]

   for interval in tree.inorder:
      for layer in layers:
         if not len(layer):
            layer.append(interval)
            break
         elif not layer[-1].is_overlapped_by_interval(interval):
            layer.append(interval)
            break

   return [IntervalTree(layer) for layer in layers]
