# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import iterate
from abjad.tools.quantizationtools.AttackPointOptimizer \
	import AttackPointOptimizer


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    r'''Concrete ``AttackPointOptimizer`` subclass which optimizes
    attack points by fusing tie leaves within logical ties with
    leaf durations decreasing monotonically.

    ``TieChains`` will be partitioned into sub-``TieChains`` if
    leaves are found with ``TempoMarks`` attached.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls naive attack-point optimizer.

        Returns none.
        '''
        for logical_tie in iterate(expr).by_logical_tie(reverse=True):
            sub_logical_ties = []
            current_sub_logical_tie = []
            for leaf in logical_tie:
                tempos = leaf._get_indicators(indicatortools.Tempo)
                if tempos:
                    if current_sub_logical_tie:
                        current_sub_logical_tie = \
                            selectiontools.LogicalTie(current_sub_logical_tie)
                        sub_logical_ties.append(current_sub_logical_tie)
                    current_sub_logical_tie = []
                current_sub_logical_tie.append(leaf)
            if current_sub_logical_tie:
                current_sub_logical_tie = selectiontools.LogicalTie(current_sub_logical_tie)
                sub_logical_ties.append(current_sub_logical_tie)
            for sub_logical_tie in sub_logical_ties:
                sub_logical_tie._fuse_leaves_by_immediate_parent()
