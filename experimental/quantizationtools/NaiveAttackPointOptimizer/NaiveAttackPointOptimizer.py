from abjad.tools import leaftools
from abjad.tools import tietools
from experimental.quantizationtools.AttackPointOptimizer import AttackPointOptimizer


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    '''Concrete ``AttackPointOptimizer`` subclass which optimizes
    attack points by fusing tie leaves within tie chains with
    leaf durations decreasing monotonically.

    Return ``NaiveAttackPointOptimizer`` instance.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for tie_chain in tietools.iterate_tie_chains_in_expr(expr, reverse=True):
            print tie_chain.prolated_duration
            leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(tie_chain)
