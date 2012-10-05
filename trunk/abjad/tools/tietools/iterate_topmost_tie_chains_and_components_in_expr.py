from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import spannertools


def iterate_topmost_tie_chains_and_components_in_expr(expr):
    r'''Iterate topemost tie chains and components forward in `expr`::

        >>> string = r"c'8 ~ c'32 d'8 ~ d'32 \times 2/3 { e'8 f'8 g'8 } a'8 ~ a'32 b'8 ~ b'32"
        >>> staff = Staff(string)

    ::

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

        >>> for x in tietools.iterate_topmost_tie_chains_and_components_in_expr(staff):
        ...     x
        ...
        TieChain((Note("c'8"), Note("c'32")))
        TieChain((Note("d'8"), Note("d'32")))
        Tuplet(2/3, [e'8, f'8, g'8])
        TieChain((Note("a'8"), Note("a'32")))
        TieChain((Note("b'8"), Note("b'32")))


    Raise tie chain error on overlapping tie chains.

    Return generator.

    .. versionchanged:: 2.0
        renamed ``iterate.chained_contents()`` to
        ``tietools.iterate_topmost_tie_chains_and_components_in_expr()``.
    '''
    from abjad.tools import tietools

    if isinstance(expr, leaftools.Leaf):
        if len(tietools.get_tie_chain(expr)) == 1:
            yield tietools.get_tie_chain(expr)
        else:
            raise TieChainError('can not have only one leaf in tie chain.')
    elif isinstance(expr, (list, containertools.Container)):
        for component in expr:
            if isinstance(component, leaftools.Leaf):
                tie_spanners = spannertools.get_spanners_attached_to_component(
                    component, tietools.TieSpanner)
                if not tie_spanners or tuple(tie_spanners)[0]._is_my_last_leaf(component):
                    yield tietools.get_tie_chain(component)
            elif isinstance(component, containertools.Container):
                yield component
    else:
        raise ValueError('input must be iterable: {!r}.'.format(expr))
