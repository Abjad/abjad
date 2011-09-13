from abjad.tools import componenttools
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_tie_chain import get_tie_chain
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def remove_all_leaves_in_tie_chain_except_first(tie_chain):
    '''Detach all leaves of tie chain after the first.
    Unspan and return length-1 tie chain.

    .. versionchanged:: 2.0
        renamed ``tietools.truncate()`` to
        ``tietools.remove_all_leaves_in_tie_chain_except_first()``.
    '''

    assert is_tie_chain(tie_chain)

    for leaf in tie_chain[1:]:
        componenttools.remove_component_subtree_from_score_and_spanners([leaf])

    first = tie_chain[0]

    spannertools.destroy_all_spanners_attached_to_component(first, TieSpanner)

    return get_tie_chain(first)
