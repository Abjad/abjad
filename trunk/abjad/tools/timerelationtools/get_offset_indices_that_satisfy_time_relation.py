import bisect


def get_offset_indices_that_satisfy_time_relation(
    timespan_2_start_offsets, timespan_2_stop_offsets, time_relation):
    '''.. versionadded:: 2.12

    Get offset indices that satisfy `time_relation`.
    
    .. note:: add example.
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
            offset_indices = timerelationtools.simple_inequality_to_offset_indices(
                inequality, timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets)
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
