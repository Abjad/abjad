from abjad.tools import componenttools


def get_tie_chains_masked_by_components(components):
    r'''Get tie chains masked by `components`:

    ::

        >>> staff = Staff("abj: | 2/4 c'4 d'4 ~ || 2/4 d'4 e'4 ~ || 2/4 e'4 f'4 |")
        >>> f(staff)
        \new Staff {
            {
                \time 2/4
                c'4
                d'4 ~
            }
            {
                d'4
                e'4 ~
            }
            {
                e'4
                f'4
            }
        }

    ::

        >>> for tie_chain in tietools.get_tie_chains_masked_by_components(staff.leaves):
        ...     tie_chain
        ...
        TieChain(Note("c'4"),)
        TieChain(Note("d'4"), Note("d'4"))
        TieChain(Note("e'4"), Note("e'4"))
        TieChain(Note("f'4"),)

    ::

        >>> for tie_chain in tietools.get_tie_chains_masked_by_components(staff[1].leaves):
        ...     tie_chain
        ...
        TieChain(Note("d'4"),)
        TieChain(Note("e'4"),)

    ::

        >>> for tie_chain in tietools.get_tie_chains_masked_by_components(staff[1:]):
        ...     tie_chain
        ...
        TieChain(Note("d'4"),)
        TieChain(Note("e'4"), Note("e'4"))
        TieChain(Note("f'4"),)

    Return list of zero or more (possibly masked) tie chains.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tietools

    assert componenttools.all_are_components(components)

    leaves_in_components = set(iterationtools.iterate_leaves_in_expr(components))

    tie_chains = []
    for leaf in leaves_in_components:
        tie_chain = tietools.get_tie_chain(leaf)
        if tie_chain not in tie_chains:
            tie_chains.append(tie_chain)

    result = []
    for tie_chain in tie_chains:
        leaves_in_tie_chain = set(iterationtools.iterate_leaves_in_expr(tie_chain))
        leaves_intersecting = leaves_in_components.intersection(leaves_in_tie_chain)
        result.append(tietools.TieChain(tuple(sorted(leaves_intersecting,
            key=lambda x: x.timespan.start_offset))))
    result.sort(key=lambda x: x[0].timespan.start_offset)

    return result

