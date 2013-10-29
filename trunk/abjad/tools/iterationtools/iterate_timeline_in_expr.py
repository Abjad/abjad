# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import leaftools


def iterate_timeline_in_expr(expr, component_class=None, reverse=False):
    r'''Iterate timeline forward in `expr`:

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

        >>> for leaf in iterationtools.iterate_timeline_in_expr(score):
        ...     leaf
        ...
        Note("c'4")
        Note("g'8")
        Note("a'8")
        Note("d'4")
        Note("b'8")
        Note("c''8")
        Note("e'4")
        Note("f'4")

    Iterate timeline backward in `expr`:

    ::

    ::

        >>> for leaf in iterationtools.iterate_timeline_in_expr(
        ...     score, reverse=True):
        ...     leaf
        ...
        Note("f'4")
        Note("e'4")
        Note("d'4")
        Note("c''8")
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Iterate leaves when `component_class` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools import scoretools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    if component_class is None:
        component_class = leaftools.Leaf

    component_generator = iterationtools.iterate_components_in_expr(
        expr, component_class=component_class)
    components = list(component_generator)

    def _backward_sort_helper(component_1, component_2):
        result = cmp(
            component_1._get_timespan().stop_offset,
            component_2._get_timespan().stop_offset)
        if result == 0:
            return cmp(
                component_1._get_parentage().score_index,
                component_2._get_parentage().score_index)
        else:
            # note negative result of cmp() is returned
            # for backward time sort
            return -result

    def _forward_sort_helper(component_1, component_2):
        result = cmp(
            component_1._get_timespan().start_offset,
            component_2._get_timespan().start_offset)
        if result == 0:
            return cmp(
                component_1._get_parentage().score_index,
                component_2._get_parentage().score_index)
        else:
            return result

    if not reverse:
        components.sort(_forward_sort_helper)
    else:
        components.sort(_backward_sort_helper)

    for component in components:
        yield component
