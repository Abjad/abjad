import bisect


def simple_inequality_to_offset_indices(simple_inequality, timespan_1,
    timespan_2_start_offsets, timespan_2_stop_offsets):

    # check input
    assert isinstance(simple_inequality, str), repr(simple_inequality)
    leftmost_index, rightmost_index = None, None

    # 1.a
    if simple_inequality == 'timespan_1.start == timespan_2.start':
        try:
            leftmost_index = _find_index(timespan_2_start_offsets, timespan_1.start_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 1.b
    elif simple_inequality == 'timespan_1.start < timespan_2.start':
        try:
            leftmost_index = _find_index_gt(timespan_2_start_offsets, timespan_1.start_offset)
            rightmost_index = len(timespan_2_start_offsets)
        except ValueError:
            pass
    # 1.c
    elif simple_inequality == 'timespan_1.start <= timespan_2.start':
        try:
            leftmost_index = _find_index_ge(timespan_2_start_offsets, timespan_1.start_offset)
            rightmost_index = len(timespan_2_start_offsets)
        except ValueError:
            pass
    # 2.a
    elif simple_inequality == 'timespan_1.start == timespan_2.stop':
        try:
            leftmost_index = _find_index(timespan_2_stop_offsets, timespan_1.start_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 2.b
    elif simple_inequality == 'timespan_1.start < timespan_2.stop':
        try:
            leftmost_index = _find_index_gt(timespan_2_stop_offsets, timespan_1.start_offset)
            rightmost_index = len(timespan_2_stop_offsets)
        except ValueError:
            pass
    # 2.c
    elif simple_inequality == 'timespan_1.start <= timespan_2.stop':
        try:
            leftmost_index = _find_index_ge(timespan_2_stop_offsets, timespan_1.start_offset)
            rightmost_index = len(timespan_2_stop_offsets)
        except ValueError:
            pass
    # 3.a
    elif simple_inequality == 'timespan_1.stop == timespan_2.start':
        try:
            leftmost_index = _find_index(timespan_2_start_offsets, timespan_1.stop_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 3.b
    elif simple_inequality == 'timespan_1.stop < timespan_2.start':
        try:
            leftmost_index = _find_index_gt(timespan_2_start_offsets, timespan_1.stop_offset)
            rightmost_index = len(timespan_2_start_offsets)
        except ValueError:
            pass
    # 3.c
    elif simple_inequality == 'timespan_1.stop <= timespan_2.start':
        try:
            leftmost_index = _find_index_ge(timespan_2_start_offsets, timespan_1.stop_offset)
            rightmost_index = len(timespan_2_start_offsets)
        except ValueError:
            pass
    # 4.a
    elif simple_inequality == 'timespan_1.stop == timespan_2.stop':
        try:
            leftmost_index = _find_index(timespan_2_start_offsets, timespan_1.stop_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 4.b
    elif simple_inequality == 'timespan_1.stop < timespan_2.stop':
        try:
            leftmost_index = _find_index_gt(timespan_2_stop_offsets, timespan_1.stop_offset)
            rightmost_index = len(timespan_2_stop_offsets)
        except ValueError:
            pass
    # 4.c
    elif simple_inequality == 'timespan_1.stop <= timespan_2.stop':
        try:
            leftmost_index = _find_index_ge(timespan_2_stop_offsets, timespan_1.stop_offset)
            rightmost_index = len(timespan_2_stop_offsets)
        except ValueError:
            pass
    # 5.a
    elif simple_inequality == 'timespan_2.start == timespan_1.start':
        try:
            leftmost_index = _find_index(timespan_2_start_offsets, timespan_1.start_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 5.b
    elif simple_inequality == 'timespan_2.start < timespan_1.start':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset < timespan_1.start_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 5.c
    elif simple_inequality == 'timespan_2.start <= timespan_1.start':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset <= timespan_1.start_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 6.a
    elif simple_inequality == 'timespan_2.start == timespan_1.stop':
        try:
            leftmost_index = _find_index(timespan_2_start_offsets, timespan_1.stop_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 6.b 
    elif simple_inequality == 'timespan_2.start < timespan_1.stop':
        try:
            leftmost_index = 0
            rightmost_index = _find_index_ge(timespan_2_start_offsets, timespan_1.stop_offset)
        except ValueError:
            pass
    # 6.c 
    elif simple_inequality == 'timespan_2.start <= timespan_1.stop':
        for i, start_offset in enumerate(reversed(timespan_2_start_offsets)):
            if start_offset <= timespan_1.stop_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_start_offsets) - i
                break
        else:
            return []
    # 7.a
    elif simple_inequality == 'timespan_2.stop == timespan_1.start':
        try:
            leftmost_index = _find_index(timespan_2_stop_offsets, timespan_1.start_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 7.b
    elif simple_inequality == 'timespan_2.stop < timespan_1.start':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset < timespan_1.start_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 7.c
    elif simple_inequality == 'timespan_2.stop <= timespan_1.start':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset <= timespan_1.start_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 8.a
    elif simple_inequality == 'timespan_2.stop == timespan_1.stop':
        try:
            leftmost_index = _find_index(timespan_2_stop_offsets, timespan_1.stop_offset)
            rightmost_index = leftmost_index + 1
        except ValueError:
            pass
    # 8.b
    elif simple_inequality == 'timespan_2.stop < timespan_1.stop':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset < timespan_1.stop_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    # 8.c
    elif simple_inequality == 'timespan_2.stop <= timespan_1.stop':
        for i, stop_offset in enumerate(reversed(timespan_2_stop_offsets)):
            if stop_offset <= timespan_1.stop_offset:
                leftmost_index = 0
                rightmost_index = len(timespan_2_stop_offsets) - i
                break
        else:
            return []
    else:
        raise ValueError(simple_inequality)

    if leftmost_index is not None and rightmost_index is not None:
        return leftmost_index, rightmost_index
    else:
        return []


### BISECT CONVENIENCE FUNCTIONS ###

def _index(a, x):
    '''Find index of leftmost value exactly equal to x.
    '''
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def _find_index_lt(a, x):
    '''Find index of rightmost value less than x.
    '''
    i = bisect.bisect_left(a, x)
    if i:
        #return a[i-1]
        return i - 1
    raise ValueError

def _find_index_le(a, x):
    '''Find index of rightmost value less than or equal to x.
    '''
    i = bisect.bisect_right(a, x)
    if i:
        #return a[i-1]
        return i - 1
    raise ValueError

def _find_index_gt(a, x):
    '''Find index of leftmost value greater than x.
    '''
    i = bisect.bisect_right(a, x)
    if i != len(a):
        #return a[i]
        return i
    raise ValueError

def _find_index_ge(a, x):
    '''Find index of leftmost item greater than or equal to x.
    '''
    i = bisect.bisect_left(a, x)
    if i != len(a):
        #return a[i]
        return i 
    raise ValueError
