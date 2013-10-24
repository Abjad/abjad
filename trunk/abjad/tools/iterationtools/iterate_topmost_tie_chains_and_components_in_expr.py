# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import selectiontools
from abjad.tools import spannertools


def iterate_topmost_tie_chains_and_components_in_expr(expr):
    r'''Iterate topmost tie chains and components forward in `expr`:

    ::

        >>> string = r"c'8 ~ c'32 d'8 ~ d'32 \times 2/3 { e'8 f'8 g'8 } a'8 ~ a'32 b'8 ~ b'32"
        >>> staff = Staff(string)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'32
            d'8 ~
            d'32
            \times 2/3 {
                e'8
                f'8
                g'8
            }
            a'8 ~
            a'32
            b'8 ~
            b'32
        }

    ::

        >>> for x in \
        ...     iterationtools.iterate_topmost_tie_chains_and_components_in_expr(
        ...     staff):
        ...     x
        ...
        TieChain(Note("c'8"), Note("c'32"))
        TieChain(Note("d'8"), Note("d'32"))
        Tuplet(2/3, [e'8, f'8, g'8])
        TieChain(Note("a'8"), Note("a'32"))
        TieChain(Note("b'8"), Note("b'32"))

    Raise tie chain error on overlapping tie chains.

    Returns generator.
    '''
    from abjad.tools import spannertools

    spanner_classes = (spannertools.TieSpanner,)
    if isinstance(expr, leaftools.Leaf):
        tie_chain = expr._get_tie_chain()
        if len(tie_chain) == 1:
            yield tie_chain
        else:
            message = 'can not have only one leaf in tie chain.'
            raise TieChainError(message)
    elif isinstance(
        expr, (list, containertools.Container, selectiontools.SliceSelection)):
        for component in expr:
            if isinstance(component, leaftools.Leaf):
                tie_spanners = component._get_spanners(spanner_classes)
                if not tie_spanners or \
                    tuple(tie_spanners)[0]._is_my_last_leaf(component):
                    yield component._get_tie_chain()
            elif isinstance(component, containertools.Container):
                yield component
    else:
        message = 'input must be iterable: {!r}.'.format(expr)
        raise ValueError(message)
