from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools.leaftools.duration_change import duration_change


## TODO: Implement leaf_fractured_at_duration( ), leaf_unfractured_at_duration( ) to parallel container split logic. Then generalize to all components. ##

def _leaf_at_duration(leaf, split_dur, spanners = 'unfractured'):
   '''Split leaf into left and right lists.
      Left list may be list of one note, many tied notes, or tuplet.
      Right list may be list of one note, many tied notes, or tuplet.'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)

   leaf_written_duration = leaf.duration.written
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur <= 0:
      return (leaf, )
   if leaf_written_duration <= unprolated_split_dur:
      return (leaf, )

   new_leaf = clone.unspan([leaf])[0]
   leaf.splice([new_leaf])
   new_leaf.grace.before = None
   new_leaf.articulations = None
   new_leaf.dynamics.mark = None
   leaf.grace.after = None

   leaf_list_1 = duration_change(leaf, unprolated_split_dur)
   leaf_list_2 = duration_change(new_leaf, leaf_written_duration - unprolated_split_dur)

   if spanners == 'fractured':
      leaf_list_1[-1].spanners.fracture(direction = 'right')
   elif spanners == 'unfractured':
      pass
   else:
      raise ValueError("keyword must be 'fractured' or 'unfractured'.")

   return leaf_list_1, leaf_list_2
