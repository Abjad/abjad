from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def group_tangent_or_overlapping_intervals_and_yield_groups(intervals):
   '''Group tangent or overlapping intervals in `intervals` and
      return tuples.   
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree:
      yield IntervalTree([ ])
      return
    
   groups = [ ]
   group = [tree.inorder[0]]

   low = group[0].low
   high = group[0].high

   for i in range(1, len(tree.inorder)):
      if tree.inorder[i].low <= high:
         group.append(tree.inorder[i])
         if high < tree.inorder[i].high:
            high = tree.inorder[i].high
      else:
         groups.append(group)
         group = [tree.inorder[i]]
         low = group[0].low
         high = group[0].high

   if group not in groups:
      groups.append(group)

   for x in groups:               
      yield tuple(x)
