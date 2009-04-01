from abjad.helpers.retroiterate import retroiterate
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
import math


def leaves_meiose(expr, n = 2):
   '''Iterate expr and replace every leaf 
      with n leaves *in the same time*.
      Preserve parentage and spanners.

      Returns nothing.'''

   for leaf in retroiterate(expr, _Leaf):
      _leaf_meiose(leaf, n)
      


def _leaf_meiose(leaf, n = 2):
   '''Replace leaf with n instances of leaf.
      Decrease duration half for each generation.
      Preserve parentage and spanners.'''

   assert isinstance(leaf, _Leaf)
   assert int(math.log(n, 2)) == math.log(n, 2)
   assert n > 0

   ## TODO: Replace with copy_unspanned(leaf, n - 1)
   new_leaves = leaf * (n - 1)
   _withdraw_from_attached_spanners(new_leaves)
   leaf.splice(new_leaves)
   adjustment_multiplier = Rational(1, n)
   leaf.duration.written *= adjustment_multiplier
   for new_leaf in new_leaves:
      new_leaf.duration.written *= adjustment_multiplier
