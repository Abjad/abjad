from abjad.checks._Check import _Check
from abjad.tools import durationtools


class MisrepresentedFlagCheck(_Check):

    def _run(self, expr):
        from abjad.tools import leaftools
        violators = [ ]
        total = 0
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            total += 1
            flags = durationtools.rational_to_flag_count(leaf.written_duration)
            #if leaf.beam.counts is None:
            #   left, right = None, None
            #else:
            #   left, right = leaf.beam.counts
            left = getattr(leaf.set, 'stem_left_beam_count', None)
            right = getattr(leaf.set, 'stem_right_beam_count', None)
            if left is not None:
                if flags < left or (left < flags and right not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if flags < right or (right < flags and left not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, total
