from abjad.tools import componenttools


def iterate_namesakes_from_component(component, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 1.1

    Iterate namesakes forward from `component`::

        >>> container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
        >>> container.is_parallel = True
        >>> container[0].name = 'staff 1'
        >>> container[1].name = 'staff 2'
        >>> score = Score([])
        >>> score.is_parallel = False
        >>> score.extend(container * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    ::

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

        >>> for staff in iterationtools.iterate_namesakes_from_component(score[0][0]):
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

    Iterate namesakes backward from `component`::

    ::

        >>> for staff in iterationtools.iterate_namesakes_from_component(score[-1][0], reverse=True):
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

    Return generator.
    '''
    from abjad.tools import iterationtools

    def _forward_helper(component):
        next_component = componenttools.get_nth_component_in_time_order_from_component(component, 1)
        if next_component is None:
            return
        dfs = iterationtools.iterate_components_depth_first(next_component, capped=False)
        for node in dfs:
            if type(node) == type(component) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(component):
                return node

    def _backward_helper(component):
        prev = componenttools.get_nth_component_in_time_order_from_component(component, -1)
        if prev is None:
            return
        dfs = iterationtools.iterate_components_depth_first(prev, capped=False, direction=Right)
        for node in dfs:
            if type(node) == type(component) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(component):
                return node

    cur_component = component
    total_components = 0

    if reverse:
        _helper = _backward_helper
    else:
        _helper = _forward_helper

    while cur_component is not None:
        if start <= total_components:
            if stop is not None:
                if total_components < stop:
                    yield cur_component
            else:
                yield cur_component
        total_components += 1
        cur_component = _helper(cur_component)
