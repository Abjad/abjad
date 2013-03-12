def simple_inequality_to_offset_indices(simple_inequality, timespan_1,
    timespan_2_start_offsets, timespan_2_stop_offsets):

    # check input
    assert isinstance(simple_inequality, str), repr(simple_inequality)

    # 1.a
    if simple_inequality == 'timespan_1.start == timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.start_offset < start_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 1.b
    elif simple_inequality == 'timespan_1.start < timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.start_offset < start_offset:
                start_index = i
                stop_index = len(timespan_2_start_offsets)
                break
        else:
            return []
    # 1.c
    elif simple_inequality == 'timespan_1.start <= timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.start_offset <= start_offset:
                start_index = i
                stop_index = len(timespan_2_start_offsets)
                break
        else:
            return []
    # 2.a
    elif simple_inequality == 'timespan_1.start == timespan_2.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if timespan_1.start_offset < stop_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 2.b
    elif simple_inequality == 'timespan_1.start < timespan_2.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if timespan_1.start_offset < stop_offset:
                start_index = i
                stop_index = len(timespan_2_stop_offsets)
                break
        else:
            return []
    # 2.c
    elif simple_inequality == 'timespan_1.start <= timespan_2.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if timespan_1.start_offset <= stop_offset:
                start_index = i
                stop_index = len(timespan_2_stop_offsets)
                break
        else:
            return []
    # 3.a
    elif simple_inequality == 'timespan_1.stop == timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if start_offset == timespan_1.stop_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 3.b
    elif simple_inequality == 'timespan_1.stop < timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.stop_offset < start_offset:
                start_index = i
                stop_index = len(timespan_2_start_offsets)
                break
        else:
            return []
    # 3.c
    elif simple_inequality == 'timespan_1.stop <= timespan_2.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.stop_offset <= start_offset:
                start_index = i
                stop_index = len(timespan_2_start_offsets)
                break
        else:
            return []
    # 4.a
    elif simple_inequality == 'timespan_1.stop == timespan_2.stop':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if timespan_1.stop_offset == stop_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 4.b
    elif simple_inequality == 'timespan_1.stop < timespan_2.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if timespan_1.stop_offset < stop_offset:
                start_index = i
                stop_index = len(timespan_2_stop_offsets)
                break
        else:
            return []
    # 4.c
    elif simple_inequality == 'timespan_1.stop <= timespan_2.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if timespan_1.stop_offset <= stop_offset:
                start_index = i
                stop_index = len(timespan_2_stop_offsets)
                break
        else:
            return []
    # 5.a
    elif simple_inequality == 'timespan_2.start == timespan_1.start':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if start_offset == timespan_1.start_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 5.b
    elif simple_inequality == 'timespan_2.start < timespan_1.start':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset < timespan_1.start_offset:
                start_index = 0
                stop_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 5.c
    elif simple_inequality == 'timespan_2.start <= timespan_1.start':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset <= timespan_1.start_offset:
                start_index = 0
                stop_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 6.a
    elif simple_inequality == 'timespan_2.start == timespan_1.stop':
        for i, start_offset in enumerate(timespan_2_start_offsets):
            if start_offset == timespan_1.stop_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 6.b 
    elif simple_inequality == 'timespan_2.start < timespan_1.stop':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset < timespan_1.stop_offset:
                start_index = 0
                stop_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 6.c 
    elif simple_inequality == 'timespan_2.start <= timespan_1.stop':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset <= timespan_1.stop_offset:
                start_index = 0
                stop_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 7.a
    elif simple_inequality == 'timespan_2.stop == timespan_1.start':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if stop_offset == timespan_1.start_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 7.b
    elif simple_inequality == 'timespan_2.stop < timespan_1.start':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset < timespan_1.start_offset:
                start_index = 0
                stop_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 7.c
    elif simple_inequality == 'timespan_2.stop <= timespan_1.start':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset <= timespan_1.start_offset:
                start_index = 0
                stop_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 8.a
    elif simple_inequality == 'timespan_2.stop == timespan_1.stop':
        for i, stop_offset in enumerate(timespan_2_stop_offsets):
            if stop_offset == timespan_1.stop_offset:
                start_index = i
                stop_index = i + 1
                break
        else:
            return []
    # 8.b
    elif simple_inequality == 'timespan_2.stop < timespan_1.stop':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset < timespan_1.stop_offset:
                start_index = 0
                stop_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 8.c
    elif simple_inequality == 'timespan_2.stop <= timespan_1.stop':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset <= timespan_1.stop_offset:
                start_index = 0
                stop_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    else:
        raise ValueError(simple_inequality)
    assert 0 <= start_index, repr(start_index)
    assert 0 <= stop_index, repr(stop_index)
    return start_index, stop_index
