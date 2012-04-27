from abjad.tools.tietools.TieChain import TieChain
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_tie_chain import get_tie_chain


def remove_nonfirst_leaves_in_tie_chain(tie_chain):
    r'''Remove nonfirst leaves in `tie_chain`::

        abjad> staff = Staff("c'4 ~ c'16")

    ::

        abjad> f(staff)
        \new Staff {
            c'4 ~
            c'16
        }

    ::

        abjad> tietools.remove_nonfirst_leaves_in_tie_chain(tietools.get_tie_chain(staff[0]))
        TieChain((Note("c'4"),))

    ::

        abjad> f(staff)
        \new Staff {
            c'4
        }

    Return `tie_chain`.

    .. versionchanged:: 2.0
        renamed ``tietools.truncate()`` to
        ``tietools.remove_all_leaves_in_tie_chain_except_first()``.

    .. versionchanged:: 2.9
        renamed ``tietools.remove_all_leaves_in_tie_chain_except_first()`` to
        ``tietools.remove_nonfirst_leaves_in_tie_chain()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    assert isinstance(tie_chain, TieChain)

    for leaf in tie_chain[1:]:
        componenttools.remove_component_subtree_from_score_and_spanners([leaf])

    first = tie_chain[0]
    spannertools.destroy_spanners_attached_to_component(first, TieSpanner)

    return get_tie_chain(first)
