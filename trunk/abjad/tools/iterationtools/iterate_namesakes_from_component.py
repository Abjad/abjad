# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_namesakes_from_component(
    component, reverse=False, start=0, stop=None):
    r'''Iterates namesakes from `component`.

    ..  container:: example

        **Example 1.** Iterate namesakes forward from component:

        ::

            >>> score = Score([])
            >>> score.is_simultaneous = False
            >>> container_1 = Container([Staff("c'8 d'8"), Staff("e'8 f'8")])
            >>> container_1.is_simultaneous = True
            >>> container_1[0].name = 'staff 1'
            >>> container_1[1].name = 'staff 2'
            >>> score.append(container_1)
            >>> container_2 = Container([Staff("g'8 a'8"), Staff("b'8 c''8")])
            >>> container_2.is_simultaneous = True
            >>> container_2[0].name = 'staff 1'
            >>> container_2[1].name = 'staff 2'
            >>> score.append(container_2)
            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> f(score)
            \new Score {
                <<
                    \context Staff = "staff 1" {
                        c'8
                        d'8
                    }
                    \context Staff = "staff 2" {
                        e'8
                        f'8
                    }
                >>
                <<
                    \context Staff = "staff 1" {
                        g'8
                        a'8
                    }
                    \context Staff = "staff 2" {
                        b'8
                        c''8
                    }
                >>
            }

        ::

            >>> for staff in iterationtools.iterate_namesakes_from_component(
            ...     container_1[0]):
            ...     print staff.lilypond_format
            ...
            \context Staff = "staff 1" {
                c'8
                d'8
            }
            \context Staff = "staff 1" {
                g'8
                a'8
            }

    ..  container:: example

        **Example 2.** Iterate namesakes backward from component:

        ::

            >>> for staff in iterationtools.iterate_namesakes_from_component(
            ...     container_2[0], reverse=True):
            ...     print staff.lilypond_format
            ...
            \context Staff = "staff 1" {
                g'8
                a'8
            }
            \context Staff = "staff 1" {
                c'8
                d'8
            }

    Returns generator.
    '''
    from abjad.tools import iterationtools

    def _backward_helper(component):
        previous_component = \
            componenttools.get_nth_component_in_time_order_from_component(
            component, -1)
        if previous_component is None:
            return
        dfs = iterationtools.iterate_components_depth_first(
            previous_component, capped=False, direction=Right)
        for node in dfs:
            if type(node) == type(component) and \
                node._select_parentage().parentage_signature == \
                component._select_parentage().parentage_signature:
                return node

    def _forward_helper(component):
        next_component = \
            componenttools.get_nth_component_in_time_order_from_component(
            component, 1)
        if next_component is None:
            return
        dfs = iterationtools.iterate_components_depth_first(
            next_component, capped=False)
        for node in dfs:
            if type(node) == type(component) and \
                node._select_parentage().parentage_signature == \
                component._select_parentage().parentage_signature:
                return node

    current_component = component
    total_components = 0

    if reverse:
        _helper = _backward_helper
    else:
        _helper = _forward_helper

    while current_component is not None:
        if start <= total_components:
            if stop is not None:
                if total_components < stop:
                    yield current_component
            else:
                yield current_component
        total_components += 1
        current_component = _helper(current_component)
