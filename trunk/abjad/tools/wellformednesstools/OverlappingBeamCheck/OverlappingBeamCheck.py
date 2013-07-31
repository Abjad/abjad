# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class OverlappingBeamCheck(Check):
    r'''Beams must not overlap.
    '''

    def _run(self, expr):
        violators = []
        spanner_classes = (spannertools.BeamSpanner, )
        all_beams = set()
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            beams = spannertools.get_spanners_attached_to_component(
                leaf, spanner_classes=spanner_classes)
            all_beams.update(beams)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        total = len(all_beams)
        return violators, total
