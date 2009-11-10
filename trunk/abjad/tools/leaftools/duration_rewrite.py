from abjad.leaf import _Leaf
from abjad.rational import Rational


def duration_rewrite(leaf, target):
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
