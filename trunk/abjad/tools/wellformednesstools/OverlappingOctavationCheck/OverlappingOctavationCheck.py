from abjad.tools import iterationtools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class OverlappingOctavationCheck(Check):
    r'''Octavation spanners must not overlap.
    '''

    def _run(self, expr):
        violators = []
        spanner_classes = (spannertools.OctavationSpanner, )
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            octavations = \
                spannertools.get_spanners_attached_to_any_improper_child_of_component(
                leaf, spanner_classes=spanner_classes)
            if 1 < len(octavations):
                for octavation in octavations:
                    if octavation not in violators:
                        violators.append(octavation)
        total = \
            spannertools.get_spanners_attached_to_any_improper_child_of_component(
            expr, spanner_classes=spanner_classes)
        return violators, len(total)
