from abjad._Leaf import _Leaf
from abjad.Rational import Rational
from abjad.spanners import Tie


def _split_leaf_at_duration(
   leaf, split_dur, spanners = 'unfractured', tie_after = False):
   '''Split leaf into left and right lists.
   Left list may be list of one note, many tied notes, or tuplet.
   Right list may be list of one note, many tied notes, or tuplet.
   Interpret boolean tie_after keyword as 'add tie after split'.
   Return value is always uniformly a pair of lists.
   '''
   from abjad.tools import componenttools
   from abjad.tools import tietools
   from abjad.tools.leaftools.change_leaf_preprolated_duration import \
      change_leaf_preprolated_duration

   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)

   leaf_multiplied_duration = leaf.duration.multiplied
   unprolated_split_dur = split_dur / leaf.duration.prolation
   
   ## handle split duration boundary cases
   if unprolated_split_dur <= 0:
      return ([ ], [leaf])
   if leaf_multiplied_duration <= unprolated_split_dur:
      return ([leaf], [ ])

   new_leaf = componenttools.clone_components_and_remove_all_spanners([leaf])[0]
   leaf.splice([new_leaf])
   new_leaf.grace.before = None
   new_leaf.articulations = None
   new_leaf.dynamics.mark = None
   leaf.grace.after = None

   left_leaf_list = change_leaf_preprolated_duration(leaf, unprolated_split_dur)
   right_leaf_list = change_leaf_preprolated_duration(
      new_leaf, leaf_multiplied_duration - unprolated_split_dur)

   leaf_left_of_split = left_leaf_list[-1]
   leaf_right_of_split = right_leaf_list[0]

   if spanners == 'fractured':
      leaf_left_of_split.spanners.fracture(direction = 'right')
   elif spanners == 'unfractured':
      pass
   else:
      raise ValueError("keyword must be 'fractured' or 'unfractured'.")

   if tie_after:
      tietools.apply_tie_spanner_to_leaf_pair(leaf_left_of_split, leaf_right_of_split)

   return left_leaf_list, right_leaf_list
