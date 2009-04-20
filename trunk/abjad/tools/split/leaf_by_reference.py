from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools.leaftools.duration_change import duration_change


def leaf_by_reference(leaf, split_dur):
   '''Split leaf into left and right lists.
      Left list may be list of one note, many tied notes, or tuplet.
      Right list may be list of one note, many tied notes, or tuplet.'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)

   leaf_written_duration = leaf.duration.written
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur <= 0:
      return [leaf]
   if leaf_written_duration <= unprolated_split_dur:
      return [leaf]

   new_leaf = clone.unspan([leaf])[0]
   leaf.splice([new_leaf])
   new_leaf.grace.before = None
   new_leaf.articulations = None
   new_leaf.dynamics.mark = None
   leaf.grace.after = None

   l1 = duration_change(leaf, unprolated_split_dur)
   l2 = duration_change(new_leaf, leaf_written_duration - unprolated_split_dur)
   result = [l1, l2] 

   return result
