# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate
from abjad.tools.wellformednesstools.Check import Check


class MispitchedTieCheck(Check):

    def _run(self, expr):
        r'''Check for mispitched notes.
        Do not check tied rests or skips.
        Implement chord-checking later.
        '''
        violators = []
        total = 0
        spanner_classes = (spannertools.TieSpanner,)
        for leaf in iterate(expr).by_class(scoretools.Note):
            total += 1
            spanners = leaf._get_spanners(spanner_classes)
            if spanners:
                spanner = spanners.pop()
                if not spanner._is_my_last_leaf(leaf):
                    next_leaf = leaf._get_leaf(1)
                    if next_leaf:
                        if leaf.written_pitch != next_leaf.written_pitch:
                            violators.append(leaf)
        return violators, total
