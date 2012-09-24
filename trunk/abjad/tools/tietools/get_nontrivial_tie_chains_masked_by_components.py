from abjad.tools import componenttools
from abjad.tools import spannertools


def get_nontrivial_tie_chains_masked_by_components(components):
    r'''Get nontrivial tie chains masked by `components`::

        >>> staff = Staff("c'8 ~ c'4 d'8 ~ d'4 e'4.")

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'4
            d'8 ~
            d'4
            e'4.
        }

    Return only nontrivial tie chains::

        >>> tietools.get_nontrivial_tie_chains_masked_by_components(staff.leaves)
        [TieChain((Note("c'8"), Note("c'4"))), TieChain((Note("d'8"), Note("d'4")))]

    Return 'masked' tie chains when only some notes of a tie chain are passed in::

        >>> tietools.get_nontrivial_tie_chains_masked_by_components(staff.leaves[1:2])
        [TieChain((Note("c'4"),))]


    Return list of zero or more (possibly masked) tie chains.

    .. versionchanged:: 2.9
        renamed ``tietools.get_tie_chains_in_expr()`` to
        ``tietools.get_nontrivial_tie_chains_masked_by_components()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tietools

    assert componenttools.all_are_components(components)

    # collect tie spanners
    tie_spanners = []
    for component in components:
        spanners = spannertools.get_spanners_attached_to_component(component, tietools.TieSpanner)
        if spanners:
            spanner = spanners.pop()
            if not spanner in tie_spanners:
                tie_spanners.append(spanner)

    # initialize tie chains
    result = []
    leaves_in_components = set(iterationtools.iterate_leaves_in_expr(components))
    for spanner in tie_spanners:
        leaves_intersecting = []
        for leaf in spanner.leaves:
            if leaf in leaves_in_components:
                leaves_intersecting.append(leaf)
        result.append(tietools.TieChain(tuple(leaves_intersecting)))

    # return result
    return result
