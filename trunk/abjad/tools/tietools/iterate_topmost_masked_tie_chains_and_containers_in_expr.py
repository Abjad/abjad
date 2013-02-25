from abjad.tools import containertools
from abjad.tools import leaftools


def iterate_topmost_masked_tie_chains_and_containers_in_expr(expr):
    r'''Iterate topmost tie chains and containers in `expr`, masked by `expr`:

    ::

        >>> input = "abj: | 2/4 c'4 d'4 ~ |"
        >>> input += "| 4/4 d'4 ~ 2/3 { d'4 d'4 d'4 } d'4 ~ |"
        >>> input += "| 2/4 d'4 e'4 |"
        >>> staff = Staff(input)
        >>> f(staff)
        \new Staff {
            {
                \time 2/4
                c'4
                d'4 ~
            }
            {
                \time 4/4
                d'4 ~
                \times 2/3 {
                    d'4
                    d'4
                    d'4
                }
                d'4 ~
            }
            {
                \time 2/4
                d'4
                e'4
            }
        }

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(
        ...     staff[0]): x
        ...
        TieChain(Note("c'4"),)
        TieChain(Note("d'4"),)

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(
        ...     staff[1]): x
        ...
        TieChain(Note("d'4"),)
        Tuplet(2/3, [d'4, d'4, d'4])
        TieChain(Note("d'4"),)

    ::

        >>> for x in tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(
        ...     staff[2]): x
        ...
        TieChain(Note("d'4"),)
        TieChain(Note("e'4"),)

    Return generator.
    '''

    from abjad.tools import tietools

    last_tie_chain = None
    for x in expr:
        if isinstance(x, leaftools.Leaf):
            tie_chain = tietools.get_tie_chain(x)
            if tie_chain == last_tie_chain:
                continue
            last_tie_chain = tie_chain
            new_tie_chain = []
            index = tie_chain[:].index(x)
            while index < len(tie_chain):
                leaf = tie_chain[index]
                if leaf.parent is x.parent:
                    new_tie_chain.append(leaf)
                else:
                    break
                index += 1
            yield tietools.TieChain(tuple(new_tie_chain))
        elif isinstance(x, containertools.Container):
            last_tie_chain = None
            yield x
