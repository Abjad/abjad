# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import contextualize
from abjad.tools.wellformednesstools.Check import Check


class MisrepresentedFlagCheck(Check):

    def _run(self, expr):
        violators = []
        total = 0
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            total += 1
            flags = leaf.written_duration.flag_count
            left = getattr(contextualize(leaf), 'stem_left_beam_count', None)
            right = getattr(contextualize(leaf), 'stem_right_beam_count', None)
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
