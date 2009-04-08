from abjad.tools import clone
from abjad.tools import mathtools
from abjad.tools import iterate
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
import math


def leaves_meiose(expr, n = 2):
   '''Iterate expr and replace every leaf 
      with n leaves *in the same time*.
      Preserve parentage and spanners.
      Returns nothing.'''

   for leaf in iterate.backwards(expr, _Leaf):
      _leaf_meiose(leaf, n)
      


def _leaf_meiose(leaf, n = 2):
   '''Replace leaf with n instances of leaf.
      Decrease duration half for each generation.
      Preserve parentage and spanners.'''

   assert isinstance(leaf, _Leaf)
   assert mathtools.is_power_of_two(n)
   assert 0 < n

   new_leaves = clone.unspan([leaf], n - 1)
   leaf.splice(new_leaves)
   adjustment_multiplier = Rational(1, n)
   leaf.duration.written *= adjustment_multiplier
   for new_leaf in new_leaves:
      new_leaf.duration.written *= adjustment_multiplier
