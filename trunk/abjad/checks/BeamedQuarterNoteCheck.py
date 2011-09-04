from abjad.checks._Check import _Check
from abjad.tools import durationtools


class BeamedQuarterNoteCheck(_Check):

    def _run(self, expr):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        violators = [ ]
        total = 0
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            total += 1
            #if leaf.beam.spanned:
            if spannertools.is_component_with_beam_spanner_attached(leaf):
                #beam = leaf.beam.spanner
                beam = spannertools.get_beam_spanner_attached_to_component(leaf)
                #if not beam.__class__.__name__ == 'DuratedComplexBeam':
                if not isinstance(beam, spannertools.DuratedComplexBeamSpanner):
                    flag_count = durationtools.rational_to_flag_count(leaf.written_duration)
                    if flag_count < 1:
                        violators.append(leaf)
        return violators, total
