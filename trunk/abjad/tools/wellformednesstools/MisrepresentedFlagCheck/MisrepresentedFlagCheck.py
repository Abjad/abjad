from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class MisrepresentedFlagCheck(Check):

    def _run(self, expr):
        violators = []
        total = 0
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            total += 1
            flags = leaf.written_duration.flag_count
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
