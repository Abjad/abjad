def comment_measures_in_container_with_measure_numbers(container):
    r'''.. versionadded:: 1.1

    Comment measures in `container` with measure numbers::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> measuretools.comment_measures_in_container_with_measure_numbers(staff)

    ::

        >>> f(staff)
        \new Staff {
            % start measure 1
            {
                \time 2/8
                c'8
                d'8
            }
            % stop measure 1
            % start measure 2
            {
                e'8
                f'8
            }
            % stop measure 2
            % start measure 3
            {
                g'8
                a'8
            }
            % stop measure 3
        }

    .. versionchanged:: 2.0
        renamed ``label.measure_numbers()`` to
        ``measuretools.comment_measures_in_container_with_measure_numbers()``.
    '''
    from abjad.tools import marktools
    from abjad.tools import iterationtools

    for measure in iterationtools.iterate_measures_in_expr(container):
        marktools.LilyPondComment('start measure %s' % measure.measure_number, 'before')(measure)
        marktools.LilyPondComment('stop measure %s' % measure.measure_number, 'after')(measure)
