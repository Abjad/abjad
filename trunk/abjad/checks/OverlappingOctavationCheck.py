from abjad.checks._Check import _Check
from abjad.tools.spannertools import OctavationSpanner


class OverlappingOctavationCheck(_Check):
    '''Octavation spanners must not overlap.'''

    def _run(self, expr):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        violators = [ ]
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            #octavations = leaf.spanners.contained
            #octavations = [p for p in octavations if isinstance(p, OctavationSpanner)]
            octavations = spannertools.get_spanners_attached_to_any_improper_child_of_component(
                leaf, OctavationSpanner)
            if 1 < len(octavations):
                for octavation in octavations:
                    if octavation not in violators:
                        violators.append(octavation)
        #total = [p for p in expr.spanners.contained if isinstance(p, OctavationSpanner)]
        total = spannertools.get_spanners_attached_to_any_improper_child_of_component(expr,
            OctavationSpanner)
        return violators, len(total)
