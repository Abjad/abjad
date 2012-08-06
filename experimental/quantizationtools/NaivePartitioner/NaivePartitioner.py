from abjad.tools import leaftools
from abjad.tools import tietools
from experimental.quantizationtools.Partitioner import Partitioner


class NaivePartitioner(Partitioner):

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for tie_chain in tietools.iterate_tie_chains_backward_in_expr(expr):
            leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain)
