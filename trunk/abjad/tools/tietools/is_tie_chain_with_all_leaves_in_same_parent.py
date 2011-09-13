from abjad.tools import componenttools
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def is_tie_chain_with_all_leaves_in_same_parent(expr):
    r'''True when expr is a tie chain with all leaves in same parent.

    That is, True when tie chain crosses no container boundaries,
    otherwise False.

    Example::

        abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> tietools.TieSpanner(t.leaves[1:3])
        TieSpanner(c'8, c'8)

        \new Staff {
                \time 2/8
                c'8
                c'8 ~
                \time 2/8
                c'8
                c'8
        }

        abjad> tie_chain = tietools.get_tie_chain(t.leaves[0])
        abjad> assert tietools.is_tie_chain_with_all_leaves_in_same_parent(tie_chain)
        abjad> tie_chain = tietools.get_tie_chain(t.leaves[1])
        abjad> assert not tietools.is_tie_chain_with_all_leaves_in_same_parent(tie_chain)
        abjad> tie_chain = tietools.get_tie_chain(t.leaves[2])
        abjad> assert not tietools.is_tie_chain_with_all_leaves_in_same_parent(tie_chain)
        abjad> tie_chain = tietools.get_tie_chain(t.leaves[3])
        abjad> assert tietools.is_tie_chain_with_all_leaves_in_same_parent(tie_chain)

    .. versionchanged:: 2.0
        renamed ``tietools.is_in_same_parent()`` to
        ``tietools.is_tie_chain_with_all_leaves_in_same_parent()``.
    '''

    return is_tie_chain(expr) and componenttools.all_are_components_in_same_parent(list(expr))
