from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.tools import clone
from abjad.tools import iterate
from abjad.tools import mathtools
import math


def meiose(expr, n = 2):
   r'''Iterate `expr` and replace every leaf in `expr`
   with `n` leaves of equal duration.
   Preserve parentage and spanners. Return nothing. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> leaftools.meiose(staff[1], 4)
      abjad> f(staff)
      \new Staff {
              c'8
              d'32
              d'32
              d'32
              d'32
              e'8
              f'8
      }      

   Divisions into only ``1, 2, 4, 8, 16, ...`` are allowed.
   That is, `n` must be a nonnegative integer power of 2.

   Function produces only leaves, never tuplets or other containers.
   '''

   ## can not wrap with update control because of leaf.splice( ) ##

   #expr.parentage.root._update._forbidUpdate( )
   for leaf in iterate.naive_backward_in(expr, _Leaf):
      _leaf_meiose(leaf, n)
   #expr.parentage.root._update._allowUpdate( )
   #expr.parentage.root._update._updateAll( )


def _leaf_meiose(leaf, n = 2):
   '''Replace leaf with n instances of leaf.
   Decrease duration half for each generation.
   Preserve parentage and spanners.
   '''

   #print 'meiosing %s ...' % leaf
   
   ## TODO: find a way to optimize this; either reimplement
   ## _Component.splice( ), or come up with something else.

   assert isinstance(leaf, _Leaf)
   assert mathtools.is_power_of_two(n)
   assert 0 < n

   new_leaves = clone.unspan([leaf], n - 1)
   leaf.splice(new_leaves)
   adjustment_multiplier = Rational(1, n)
   leaf.duration.written *= adjustment_multiplier
   for new_leaf in new_leaves:
      new_leaf.duration.written *= adjustment_multiplier
