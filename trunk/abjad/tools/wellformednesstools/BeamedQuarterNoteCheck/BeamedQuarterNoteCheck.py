from abjad.tools import beamtools
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
            #if leaf.beam.spanned:
            if beamtools.is_component_with_beam_spanner_attached(leaf):
                beam = beamtools.get_beam_spanner_attached_to_component(leaf)
                if not isinstance(beam, beamtools.DuratedComplexBeamSpanner):
                    flag_count = durationtools.rational_to_flag_count(leaf.written_duration)
                    if flag_count < 1:
                        violators.append(leaf)
        return violators, total
