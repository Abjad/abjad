from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools import mathtools
from abjad.tools.leaftools.scale_binary import scale_binary


def split_binary(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   leaf_written_duration = leaf.duration.written
   unprolated_split_dur = split_dur / leaf.duration.prolation
   denominator = unprolated_split_dur._d
   assert mathtools.is_power_of_two(denominator)
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
   l1 = scale_binary(leaf, unprolated_split_dur)
   l2 = scale_binary(new_leaf, leaf_written_duration - unprolated_split_dur)
   result = [l1, l2] 
   return result
