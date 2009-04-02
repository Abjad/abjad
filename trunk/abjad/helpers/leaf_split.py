from abjad.helpers.copy_unspan import copy_unspan
from abjad.helpers.leaf_scale import leaf_scale
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


def leaf_split(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur == 0 or \
      leaf.duration.written <= unprolated_split_dur:
      return [leaf]
   new_leaf = copy_unspan([leaf])[0]
   leaf.splice_left([new_leaf])
   l1 = leaf_scale(new_leaf, unprolated_split_dur)
   l2 = leaf_scale(leaf, leaf.duration.written - unprolated_split_dur)
   return [l1, l2]
