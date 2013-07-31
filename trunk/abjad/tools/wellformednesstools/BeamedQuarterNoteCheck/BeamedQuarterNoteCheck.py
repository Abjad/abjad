# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class BeamedQuarterNoteCheck(Check):

    def _run(self, expr):
        violators = []
        total = 0
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            total += 1
            if leaf._has_spanner(spannertools.BeamSpanner):
                beam = leaf._get_spanner(spannertools.BeamSpanner)
                if not isinstance(beam, spannertools.DuratedComplexBeamSpanner):
                    flag_count = leaf.written_duration.flag_count
                    if flag_count < 1:
                        violators.append(leaf)
        return violators, total
