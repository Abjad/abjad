from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


def leaf_duration_rewrite(leaf, target):
   '''Externalization of t.duration.rewrite( ).
      Return leaf.'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(target, Rational)

   #previous = leaf.multiplied
   previous = leaf.duration.multiplied
   leaf.duration.written = target
   leaf.duration.multiplier = None
   multiplier = previous / leaf.duration.written
   if multiplier != 1:
      leaf.duration.multiplier = multiplier

   return leaf
