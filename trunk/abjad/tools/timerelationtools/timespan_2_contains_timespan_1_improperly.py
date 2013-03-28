def timespan_2_contains_timespan_1_improperly(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `timespan_2` contains `timespan_1` improperly:

    ::

        >>> z(timerelationtools.timespan_2_contains_timespan_1_improperly())
        timerelationtools.TimespanTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan_2.start_offset <= timespan_1.start_offset'),
                timerelationtools.SimpleInequality('timespan_1.stop_offset <= timespan_2.stop_offset')
                ],
                logical_operator='and'
                )
            )

    Example:

    ::

        >>> staff = Staff(r"c'8. \p \< fs'16 a'4 af'8 \f \> g'8 ~ g'16 f' e' ef' \p")
        >>> timespan_1 = timespantools.Timespan(Offset(1, 4), Offset(3, 8))

    ::

        >>> offset_lists = staff[:].get_offset_lists()
        >>> time_relation = timerelationtools.timespan_2_contains_timespan_1_improperly(timespan_1=timespan_1)
        >>> start_index, stop_index = time_relation.get_offset_indices(*offset_lists)
        >>> selected_notes = staff[start_index:stop_index]
        >>> selected_notes
        Selection(Note("a'4"),)

    ::

        >>> labeltools.color_leaves_in_expr(selected_notes, 'red')
        >>> show(staff) # doctest: +SKIP

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        timerelationtools.CompoundInequality([
            'timespan_2.start_offset <= timespan_1.start_offset',
            'timespan_1.stop_offset <= timespan_2.stop_offset',
            ]),
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
