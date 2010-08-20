from abjad.checks._Check import _Check
from abjad.components._Leaf import _Leaf
from abjad.tools.spannertools import TempoSpanner
from abjad.tools import spannertools


class OverlappingTempoSpannerCheck(_Check):
   '''Tempo spanners must not overlap.'''

   def _run(self, expr):
      from abjad.tools import leaftools
      violators = set([ ])
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         #spanners_in_parentage = leaf.tempo.spanners_in_parentage
         spanners_in_parentage = \
            spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
            leaf, TempoSpanner)
         if 1 < len(spanners_in_parentage):
            violators.update(spanners_in_parentage)
      total = [p for p in expr.spanners.contained if isinstance(p, TempoSpanner)]
      return violators, len(total)
