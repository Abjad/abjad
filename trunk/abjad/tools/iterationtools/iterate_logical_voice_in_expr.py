# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_logical_voice_in_expr(
    expr, 
    component_class, 
    logical_voice_indicator, 
    reverse=False,
    ):
    r'''Yield left-to-right instances of `component_class` in `expr` 
    with `logical_voice_indicator`:

    ::

        >>> container_1 = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
        >>> container_1.is_simultaneous = True
        >>> container_1[0].name = 'voice 1'
        >>> container_1[1].name = 'voice 2'
        >>> container_2 = Container([Voice("g'8 a'8"), Voice("b'8 c''8")])
        >>> container_2.is_simultaneous = True
        >>> container_2[0].name = 'voice 1'
        >>> container_2[1].name = 'voice 2'
        >>> staff = Staff([container_1, container_2])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }

    ::

        >>> leaf = staff.select_leaves(allow_discontiguous_leaves=True)[0]
        >>> signature = inspect(leaf).get_parentage().logical_voice_indicator
        >>> for x in iterationtools.iterate_logical_voice_in_expr(
        ...     staff, Note, signature):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Return generator.
    '''
    from abjad.tools import iterationtools

    if isinstance(expr, component_class) and \
        expr._get_parentage().logical_voice_indicator == logical_voice_indicator:
        yield expr

    if not reverse:
        if isinstance(expr, (list, tuple)):
            for m in expr:
                for x in iterationtools.iterate_logical_voice_in_expr(
                    m, component_class, logical_voice_indicator):
                    yield x
        if hasattr(expr, '_music'):
            for m in expr._music:
                for x in iterationtools.iterate_logical_voice_in_expr(
                    m, component_class, logical_voice_indicator):
                    yield x
    else:
        if isinstance(expr, (list, tuple)):
            for m in reversed(expr):
                for x in iterationtools.iterate_logical_voice_in_expr(
                    m, component_class, logical_voice_indicator, reverse=True):
                    yield x
        if hasattr(expr, '_music'):
            for m in reversed(expr._music):
                for x in iterationtools.iterate_logical_voice_in_expr(
                    m, component_class, logical_voice_indicator, reverse=True):
                    yield x
