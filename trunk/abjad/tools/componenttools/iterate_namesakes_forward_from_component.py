def iterate_namesakes_forward_from_component(component, start=0, stop=None):
    r'''.. versionadded:: 1.1

    .. note: Deprecated. Use `componenttools.iterate_namesakes_from_component` instead.

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

        >>> for staff in componenttools.iterate_namesakes_forward_from_component(score[0][0]):
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

    Return generator.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_namesakes_from_component(
        component, start=start, stop=stop)
