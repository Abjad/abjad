from abjad.tools import beamtools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class BeamedQuarterNoteCheck(Check):

    def _run(self, expr):
        violators = []
        total = 0
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            total += 1
            if leaf._has_spanner(beamtools.BeamSpanner):
                beam = leaf._get_spanner(beamtools.BeamSpanner)
                if not isinstance(beam, beamtools.DuratedComplexBeamSpanner):
                    flag_count = leaf.written_duration.flag_count
                    if flag_count < 1:
                        violators.append(leaf)
        return violators, total
