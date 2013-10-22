# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_logical_voice_from_component(
    component, 
    component_class=None, 
    reverse=False,
    ):
    r'''Iterate logical voice forward from `component` and yield instances 
    of `component_class`.

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

    Starting from the first leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[0], Note):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Starting from the second leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[1], Note):
        ...     x
        ...
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Yield all components in logical voice:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[0]):
        ...     x
        ...
        Note("c'8")
        Voice-"voice 1"{2}
        Note("d'8")
        Voice-"voice 1"{2}
        Note("g'8")
        Note("a'8")

    Iterate logical voice backward from `component` and yield instances 
    of `component_class`, starting from the last leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[-1], 
        ...     Note, 
        ...     reverse=True,
        ...     ):
        ...     x
        Note("c''8")
        Note("b'8")
        Note("f'8")
        Note("e'8")

    Yield all components in logical voice:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[-1], 
        ...     reverse=True,
        ...     ):
        ...     x
        Note("c''8")
        Voice-"voice 2"{2}
        Note("b'8")
        Voice-"voice 2"{2}
        Note("f'8")
        Note("e'8")

    Returns generator.
    '''
    from abjad.tools import iterationtools

    # set default class
    if component_class is None:
        component_class = componenttools.Component

    # save logical voice signature of input component
    signature = component._get_parentage().logical_voice_indicator

    # iterate component depth-first allowing to crawl UP into score
    if not reverse:
        for x in iterationtools.iterate_components_depth_first(
            component, capped=False):
            if isinstance(x, component_class):
                if x._get_parentage().logical_voice_indicator == signature:
                    yield x
    else:
        for x in iterationtools.iterate_components_depth_first(
            component, capped=False, direction=Right):
            if isinstance(x, component_class):
                if x._get_parentage().logical_voice_indicator == signature:
                    yield x
