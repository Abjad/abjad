def iterate_namesakes_backward_from_component(component, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate namesakes backward from `component`::

        >>> container = Container(Staff(notetools.make_repeated_notes(2)) * 2)
        >>> container.is_parallel = True
        >>> container[0].name = 'staff 1'
        >>> container[1].name = 'staff 2'
        >>> score = Score([])
        >>> score.is_parallel = False
        >>> score.extend(container * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

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

        >>> for staff in componenttools.iterate_namesakes_backward_from_component(score[-1][0]):
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
    from abjad.tools import componenttools

    # TODO: Write tests because ackwards depth first search has always had a bug that needs fixing.
    def _helper(component):
        prev = componenttools.get_nth_component_in_time_order_from_component(component, -1)
        if prev is None:
            return
        dfs = componenttools.iterate_components_depth_first(prev, capped=False, direction='right')
        for node in dfs:
            if type(node) == type(component) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(component):
                return node

    cur_component = component
    total_components = 0

    while cur_component is not None:
        if start <= total_components:
            if stop is not None:
                if total_components < stop:
                    yield cur_component
            else:
                yield cur_component
        total_components += 1
        cur_component = _helper(cur_component)
