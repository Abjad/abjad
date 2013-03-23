import bisect


# TODO: implement as method bound to TimespanTimespanTimeRelation
def get_offset_indices_that_satisfy_time_relation(
    timespan_2_start_offsets, timespan_2_stop_offsets, time_relation):
    '''.. versionadded:: 2.12

    Get offset indices that satisfy `time_relation`.

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> start_offsets = [note.start_offset for note in staff]
        >>> stop_offsets = [note.stop_offset for note in staff]

    Example 1. Notes equal to ``staff[0:2]`` start during timespan ``[0, 3/16)``:

    ::

        >>> timespan_1 = timespantools.Timespan(Offset(0), Offset(3, 16))
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        >>> timerelationtools.get_offset_indices_that_satisfy_time_relation(
        ...     start_offsets, stop_offsets, time_relation)
        (0, 2)

    Example 2. Notes equal to ``staff[2:8]`` start after timespan ``[0, 3/16)`` stops:

    ::

        >>> timespan_1 = timespantools.Timespan(Offset(0), Offset(3, 16))
        >>> time_relation = timerelationtools.timespan_2_starts_after_timespan_1_stops(timespan_1=timespan_1)
        >>> timerelationtools.get_offset_indices_that_satisfy_time_relation(
        ...     start_offsets, stop_offsets, time_relation)
        (2, 8)
    
    Return nonnegative integer pair.
    '''
    from abjad.tools import timerelationtools
    from abjad.tools import timespantools
    
    # check input
    assert time_relation.inequalities, repr((time_relation, time_relation.inequalities))
    timespan_1 = time_relation.timespan_1

    # TODO: eventually allow only compound inequality of simple inequality
    if isinstance(time_relation.inequalities, timerelationtools.CompoundInequality):
        result = time_relation.inequalities.get_offset_indices(
            timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
    elif isinstance(time_relation.inequalities, list):
        start_index_stop_index_pairs = timespantools.TimespanInventory()
        for inequality in time_relation.inequalities:
            simple_inequality = timerelationtools.SimpleInequality(inequality)
            offset_indices = simple_inequality.to_offset_indices(
                timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
            start_index_stop_index_pairs.append(timespantools.Timespan(*offset_indices))
        result = start_index_stop_index_pairs.compute_logical_and()

    if not result:
        return []
    elif len(result) == 1:
        timespan = result[0]
        start_index = int(timespan.start_offset)
        stop_index = int(timespan.stop_offset)
        return start_index, stop_index
    elif 0 < len(result):
        raise Exception('inequality evaluates to disjunct range: {!r}.'.format(result))
