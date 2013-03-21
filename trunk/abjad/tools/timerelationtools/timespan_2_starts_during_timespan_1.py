def timespan_2_starts_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `timespan_2` starts during `timespan_1`:

    ::

        >>> z(timerelationtools.timespan_2_starts_during_timespan_1())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.start_offset <= timespan_2.start_offset < timespan_1.stop_offset',
            ['timespan_1.start_offset <= timespan_2.start_offset', 'timespan_2.start_offset < timespan_1.stop_offset']
            )

    Example score:

    ::

        >>> staff_1 = Staff("c'4 d'4 e'4 f'4 g'2 c''2")
        >>> staff_2 = Staff("c'2 b'2 a'2 g'2")
        >>> score = Score([staff_1, staff_2])

    ::
    
        >>> start_offsets = [note.start_offset for note in staff_1]
        >>> stop_offsets = [note.stop_offset for note in staff_1]

    ::

        >>> timespan_1 = timespantools.Timespan(Offset(1, 4), Offset(5, 4))
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
        ...     timespan_1=timespan_1)
        >>> start_index, stop_index = timerelationtools.get_offset_indices_that_satisfy_time_relation(
        ...     start_offsets, stop_offsets, time_relation)
        
    ::

        >>> selected_notes = staff_1[start_index:stop_index]
        >>> selected_notes
        Selection(Note("d'4"), Note("e'4"), Note("f'4"), Note("g'2"))

    ::

        >>> labeltools.color_leaves_in_expr(selected_notes, 'red')

    ::

        >>> show(score) # doctest: +SKIP


    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.start_offset <= timespan_2.start_offset < timespan_1.stop_offset',
        [
            'timespan_1.start_offset <= timespan_2.start_offset',
            'timespan_2.start_offset < timespan_1.stop_offset',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)


    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
