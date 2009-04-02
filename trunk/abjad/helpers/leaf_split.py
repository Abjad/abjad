from abjad.helpers.copy_unspan import copy_unspan
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.is_power_of_two import _is_power_of_two
from abjad.helpers.leaf_scale import leaf_scale
from abjad.helpers.leaf_scale import leaf_scale_binary
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


#def leaf_split(split_dur, leaf):
def leaf_split(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur == 0 or \
      leaf.duration.written <= unprolated_split_dur:
      return [leaf]
   new_leaf = copy_unspan([leaf])[0]
   leaf.splice_left([new_leaf])
   #l1 = leaf_scale(unprolated_split_dur, new_leaf)
   #l2 = leaf_scale(leaf.duration.written - unprolated_split_dur, leaf)
   l1 = leaf_scale(new_leaf, unprolated_split_dur)
   l2 = leaf_scale(leaf, leaf.duration.written - unprolated_split_dur)
   return [l1, l2]


#def leaf_split_binary(split_dur, leaf):
def leaf_split_binary(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   unprolated_split_dur = split_dur / leaf.duration.prolation
   denominator = unprolated_split_dur._d
   assert _is_power_of_two(denominator)
   if unprolated_split_dur == 0 or \
      leaf.duration.written <= unprolated_split_dur:
      return [leaf]
   new_leaf = copy_unspan([leaf])[0]
   leaf.splice([new_leaf])
   ## remove afterGrace from new_leaf and Grace from leaf (l2)
   new_leaf.grace.after = None
   leaf.grace.before = None
   ## remove articulations and dynamics
   leaf.articulations = None
   leaf.dynamics = None
   #l1 = leaf_scale_binary(unprolated_split_dur, new_leaf)
   #l2 = leaf_scale_binary(leaf.duration.written-unprolated_split_dur, leaf)
   l1 = leaf_scale_binary(new_leaf, unprolated_split_dur)
   l2 = leaf_scale_binary(leaf, leaf.duration.written-unprolated_split_dur)
   result = [l1, l2] 
   return result
