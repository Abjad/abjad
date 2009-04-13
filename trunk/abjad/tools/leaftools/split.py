from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools.leaftools.scale import scale


def split(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur == 0 or \
      leaf.duration.written <= unprolated_split_dur:
      return [leaf]
   new_leaf = clone.unspan([leaf])[0]
   leaf.splice_left([new_leaf])
   l1 = scale(new_leaf, unprolated_split_dur)
   l2 = scale(leaf, leaf.duration.written - unprolated_split_dur)
   return [l1, l2]
