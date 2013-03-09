# TODO: eventually implement this as method bound to some type of selection class
def get_counttime_components_that_satisfy_time_relation(counttime_components, time_relation):
    '''.. versionadded:: 2.12

    Get `counttime_components` that satisfy `time_relation`:

    ::

        >>> voice = Voice([Note(i % 36, Duration(1, 4)) for i in range(200)])
        >>> timespan_1 = timespantools.Timespan(20, 22)
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)

    ::

        >>> result = timerelationtools.get_counttime_components_that_satisfy_time_relation(
        ...     voice[:], time_relation)

    ::

        >>> for counttime_component in result: 
        ...     counttime_component
        Note("af'4")
        Note("a'4")
        Note("bf'4")
        Note("b'4")
        Note("c''4")
        Note("cs''4")
        Note("d''4")
        Note("ef''4")

    ::

        >>> result.timespan
        Timespan(start_offset=Offset(20, 1), stop_offset=Offset(22, 1))

    `counttime_components` must belong to a single voice.

    `counttime_components` must be time-contiguous.

    Example shown here takes 181337 function calls under r9683.

    Return selection.
    '''
    from abjad.tools import selectiontools
    from abjad.tools import timerelationtools

    # check input
    assert isinstance(counttime_components, (list, selectiontools.Selection)), repr(counttime_components)
    assert isinstance(time_relation, timerelationtools.TimeRelation), repr(time_relation)
    assert time_relation.timespan_1 is not None

    # iterate counttime components
    result = []
    for counttime_component in counttime_components:
        if time_relation(timespan_2=counttime_component.timespan):
            result.append(counttime_component)

    # return result
    return selectiontools.Selection(result)
