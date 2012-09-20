from abjad.tools import iterationtools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class OverlappingOctavationCheck(Check):
    '''Octavation spanners must not overlap.'''

    def _run(self, expr):
        violators = []
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            #octavations = leaf.spanners.contained
            #octavations = [p for p in octavations if isinstance(p, OctavationSpanner)]
            octavations = spannertools.get_spanners_attached_to_any_improper_child_of_component(
                leaf, spannertools.OctavationSpanner)
            if 1 < len(octavations):
                for octavation in octavations:
                    if octavation not in violators:
                        violators.append(octavation)
        #total = [p for p in expr.spanners.contained if isinstance(p, OctavationSpanner)]
        total = spannertools.get_spanners_attached_to_any_improper_child_of_component(expr,
            spannertools.OctavationSpanner)
        return violators, len(total)
