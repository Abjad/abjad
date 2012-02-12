from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_leaves_in_tie_chain(tie_chain):
    '''Return Python list of leaves in tie chain.
    '''

    assert is_tie_chain(tie_chain)

    try:
        #return tie_chain[0].tie.spanner.leaves
        tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
            tie_chain[0], TieSpanner)
        return tie_spanner.leaves
    except MissingSpannerError:
        assert len(tie_chain) == 1
        leaves = (tie_chain[0], )
        return leaves
