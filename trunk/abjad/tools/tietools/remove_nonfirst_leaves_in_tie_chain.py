from abjad.tools import componenttools
from abjad.tools import spannertools


def remove_nonfirst_leaves_in_tie_chain(tie_chain):
    r'''Remove nonfirst leaves in `tie_chain`::

        >>> staff = Staff("c'4 ~ c'16")

    ::

        >>> f(staff)
        \new Staff {
            c'4 ~
            c'16
        }

    ::

        >>> tietools.remove_nonfirst_leaves_in_tie_chain(tietools.get_tie_chain(staff[0]))
        TieChain((Note("c'4"),))

    ::

        >>> f(staff)
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
    from abjad.tools import tietools

    assert isinstance(tie_chain, tietools.TieChain)

    for leaf in tie_chain[1:]:
        componenttools.remove_component_subtree_from_score_and_spanners([leaf])

    first = tie_chain[0]
    spannertools.destroy_spanners_attached_to_component(first, tietools.TieSpanner)

    return tietools.get_tie_chain(first)
