from abjad.leaf.leaf import _Leaf
from abjad.tools import clone
from abjad.tools import iterate


def multiply(expr, total = 1):
   '''Insert n copies of each leaf l_i after l_i in expr.
      preserve parentage and spanners.'''

   for leaf in iterate.naive_backward(expr, _Leaf):
      leaf.splice(clone.unspan([leaf], total - 1))
