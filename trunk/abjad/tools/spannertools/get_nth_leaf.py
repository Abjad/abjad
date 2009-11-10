from abjad.leaf import _Leaf
from abjad.spanners import Spanner
from abjad.tools.spannertools.iterate_components_forward import \
   iterate_components_forward as spannertools_iterate_components_forward
from abjad.tools.spannertools.iterate_components_backward import \
   iterate_components_backward as spannertools_iterate_components_backward


def get_nth_leaf(spanner, idx):
   '''Get nth leaf in spanner, no matter how complicated the nesting
   situation.

   '''

   if not isinstance(idx, (int, long)):
      raise TypeError

   if 0 <= idx:
      leaves = spannertools_iterate_components_forward(spanner, klass = _Leaf)
      for leaf_index, leaf in enumerate(leaves):
         if leaf_index == idx:
            return leaf
   else:
      leaves = spannertools_iterate_components_backward(spanner, klass = _Leaf)
      for leaf_index, leaf in enumerate(leaves):
         leaf_number = -leaf_index - 1
         if leaf_number == idx:
            return leaf

   raise IndexError
