from abjad.checks._Check import _Check
from abjad.tools.spannertools import BeamSpanner


class OverlappingBeamCheck(_Check):
    '''Beams must not overlap.
    '''

    def _run(self, expr):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        violators = [ ]
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            #beams = [p for p in leaf.spanners.attached
            #   if isinstance(p, BeamSpanner)]
            beams = spannertools.get_spanners_attached_to_component(leaf, BeamSpanner)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        #total = len([p for p in expr.spanners.contained if isinstance(p, BeamSpanner)])
        total = len(spannertools.get_spanners_attached_to_component(expr, BeamSpanner))
        return violators, total
