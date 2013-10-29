# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import leaftools


def iterate_timeline_from_component(expr, component_class=None, reverse=False):
    r'''Iterate timeline forward from `component`:

    ::

        >>> score = Score([])
        >>> score.append(Staff("c'4 d'4 e'4 f'4"))
        >>> score.append(Staff("g'8 a'8 b'8 c''8"))

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>

    ::

        >>> for leaf in iterationtools.iterate_timeline_from_component(
        ...     score[1][2]):
        ...     leaf
        ...
        Note("b'8")
        Note("c''8")
        Note("e'4")
        Note("f'4")

    Iterate timeline backward from `component`:

    ::

    ::

        >>> for leaf in iterationtools.iterate_timeline_from_component(
        ...     score[1][2], reverse=True):
        ...     leaf
        ...
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Yield components sorted backward by score offset stop time 
    when `reverse` is True.

    Iterate leaves when `component_class` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools import iterationtools

    if component_class is None:
        component_class = leaftools.Leaf

    component_generator = iterationtools.iterate_timeline_in_expr(
        expr._get_parentage().root, 
        component_class=component_class,
        reverse=reverse,
        )

    yielded_expr = False
    for component in component_generator:
        if yielded_expr:
            yield component
        elif component is expr:
            yield component
            yielded_expr = True
