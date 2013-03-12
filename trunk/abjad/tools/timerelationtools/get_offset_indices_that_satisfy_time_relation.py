import bisect


def get_offset_indices_that_satisfy_time_relation(
    timespan_2_start_offsets, timespan_2_stop_offsets, time_relation):
    '''.. versionadded:: 2.12

    Get offset indices that satisfy `time_relation`.
    
    .. note:: add example.
    '''
    from abjad.tools import timespantools
    
    # check input
    assert time_relation.inequalities, repr((time_relation, time_relation.inequalities))
    timespan_1 = time_relation.timespan_1
    #print time_relation.storage_format

    # generate one start index / stop index pair per inequality
    start_index_stop_index_pairs = timespantools.TimespanInventory()
    for inequality in time_relation.inequalities:
        # 1.a
        if inequality == 'timespan_1.start == timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.start_offset < start_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 1.b
        elif inequality == 'timespan_1.start < timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.start_offset < start_offset:
                    start_index = i
                    stop_index = len(timespan_2_start_offsets)
                    break
            else:
                return []
        # 1.c
        elif inequality == 'timespan_1.start <= timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.start_offset <= start_offset:
                    start_index = i
                    stop_index = len(timespan_2_start_offsets)
                    break
            else:
                return []
        # 2.a
        elif inequality == 'timespan_1.start == timespan_2.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if timespan_1.start_offset < stop_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 2.b
        elif inequality == 'timespan_1.start < timespan_2.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if timespan_1.start_offset < stop_offset:
                    start_index = i
                    stop_index = len(timespan_2_stop_offsets)
                    break
            else:
                return []
        # 2.c
        elif inequality == 'timespan_1.start <= timespan_2.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if timespan_1.start_offset <= stop_offset:
                    start_index = i
                    stop_index = len(timespan_2_stop_offsets)
                    break
            else:
                return []
        # 3.a
        elif inequality == 'timespan_1.stop == timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if start_offset == timespan_1.stop_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 3.b
        elif inequality == 'timespan_1.stop < timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.stop_offset < start_offset:
                    start_index = i
                    stop_index = len(timespan_2_start_offsets)
                    break
            else:
                return []
        # 3.c
        elif inequality == 'timespan_1.stop <= timespan_2.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.stop_offset <= start_offset:
                    start_index = i
                    stop_index = len(timespan_2_start_offsets)
                    break
            else:
                return []
        # 4.a
        elif inequality == 'timespan_1.stop == timespan_2.stop':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if timespan_1.stop_offset == stop_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 4.b
        elif inequality == 'timespan_1.stop < timespan_2.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if timespan_1.stop_offset < stop_offset:
                    start_index = i
                    stop_index = len(timespan_2_stop_offsets)
                    break
            else:
                return []
        # 4.c
        elif inequality == 'timespan_1.stop <= timespan_2.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if timespan_1.stop_offset <= stop_offset:
                    start_index = i
                    stop_index = len(timespan_2_stop_offsets)
                    break
            else:
                return []
        # 5.a
        elif inequality == 'timespan_2.start == timespan_1.start':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if start_offset == timespan_1.start_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 5.b
        elif inequality == 'timespan_2.start < timespan_1.start':
            for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
                if start_offset < timespan_1.start_offset:
                    start_index = 0
                    stop_index = len(timespan_2_start_offsets) - i
                    break
            else:
                return []
        # 5.c
        elif inequality == 'timespan_2.start <= timespan_1.start':
            for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
                if start_offset <= timespan_1.start_offset:
                    start_index = 0
                    stop_index = len(timespan_2_start_offsets) - i
                    break
            else:
                return []
        # 6.a
        elif inequality == 'timespan_2.start == timespan_1.stop':
            for i, start_offset in enumerate(timespan_2_start_offsets):
                if start_offset == timespan_1.stop_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 6.b 
        elif inequality == 'timespan_2.start < timespan_1.stop':
            for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
                if start_offset < timespan_1.stop_offset:
                    start_index = 0
                    stop_index = len(timespan_2_start_offsets) - i
                    break
            else:
                return []
        # 6.c 
        elif inequality == 'timespan_2.start <= timespan_1.stop':
            for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
                if start_offset <= timespan_1.stop_offset:
                    start_index = 0
                    stop_index = len(timespan_2_start_offsets) - i
                    break
            else:
                return []
        # 7.a
        elif inequality == 'timespan_2.stop == timespan_1.start':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if stop_offset == timespan_1.start_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 7.b
        elif inequality == 'timespan_2.stop < timespan_1.start':
            for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
                if stop_offset < timespan_1.start_offset:
                    start_index = 0
                    stop_index = len(timespan_2_stop_offsets) - i
                    break
            else:
                return []
        # 7.c
        elif inequality == 'timespan_2.stop <= timespan_1.start':
            for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
                if stop_offset <= timespan_1.start_offset:
                    start_index = 0
                    stop_index = len(timespan_2_stop_offsets) - i
                    break
            else:
                return []
        # 8.a
        elif inequality == 'timespan_2.stop == timespan_1.stop':
            for i, stop_offset in enumerate(timespan_2_stop_offsets):
                if stop_offset == timespan_1.stop_offset:
                    start_index = i
                    stop_index = i + 1
                    break
            else:
                return []
        # 8.b
        elif inequality == 'timespan_2.stop < timespan_1.stop':
            for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
                if stop_offset < timespan_1.stop_offset:
                    start_index = 0
                    stop_index = len(timespan_2_stop_offsets) - i
                    break
            else:
                return []
        # 8.c
        elif inequality == 'timespan_2.stop <= timespan_1.stop':
            for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
                if stop_offset <= timespan_1.stop_offset:
                    start_index = 0
                    stop_index = len(timespan_2_stop_offsets) - i
                    break
            else:
                return []
        else:
            raise ValueError(inequality)
        assert 0 <= start_index, repr(start_index)
        assert 0 <= stop_index, repr(stop_index)
        start_index_stop_index_pairs.append(timespantools.Timespan(start_index, stop_index))

    #print start_index_stop_index_pairs.storage_format
    result = start_index_stop_index_pairs.compute_logical_and()
    if result:
        timespan = result[0]
        start_index = int(timespan.start_offset)
        stop_index = int(timespan.stop_offset)
        return start_index, stop_index
    else:
        return []
