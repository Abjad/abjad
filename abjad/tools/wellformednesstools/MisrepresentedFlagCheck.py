# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class MisrepresentedFlagCheck(Check):

    def _run(self, expr):
        violators = []
        total = 0
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            total += 1
            flags = leaf.written_duration.flag_count
            left = getattr(leaf.set, 'stem_left_beam_count', None)
            right = getattr(leaf.set, 'stem_right_beam_count', None)
            if left is not None:
                if flags < left or \
                    (left < flags and right not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if flags < right or \
                    (right < flags and left not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, total
