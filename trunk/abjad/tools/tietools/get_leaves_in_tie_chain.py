from abjad.tools import spannertools
from abjad.tools.tietools.TieChain import TieChain
from abjad.tools.tietools.TieSpanner import TieSpanner


def get_leaves_in_tie_chain(tie_chain):
    '''Return Python list of leaves in tie chain.
    '''

    assert isinstance(tie_chain, TieChain)

    try:
        tie_spanner = spannertools.get_the_only_spanner_attached_to_component(tie_chain[0], TieSpanner)
        return tie_spanner.leaves
    except MissingSpannerError:
        assert len(tie_chain) == 1
        leaves = (tie_chain[0], )
        return leaves
