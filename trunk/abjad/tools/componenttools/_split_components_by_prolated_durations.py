from abjad.tools.componenttools._split_component_at_duration import _split_component_at_duration
from abjad.tools import durationtools


# TODO: Take care of bug that unintentionally fractures ties. #

def _split_components_by_prolated_durations(components, durations,
    spanners = 'unfractured', cyclic = False, tie_after = False):
    '''Partition Python list of components according to durations.
        Interpret durations as prolated durations.
        Return list of newly split parts.
    '''
    from abjad.tools import componenttools

    # check input
    assert componenttools.all_are_components(components)
    assert isinstance(durations, list)
    assert all([isinstance(x, (int, float, durationtools.Duration)) for x in durations])

    # initialize loop variables
    result = []
    part = []
    duration_index = 0
    len_durations = len(durations)
    cum_duration = durationtools.Duration(0)
    xx = list(components[:])

    # loop and build partition parts
    # grab next component from input stack every time through loop
    # grab size of current part every time, though part may still be filling
    while True:
        #print 'xx are now %s' % xx
        try:
            if cyclic:
                next_split_point = durations[duration_index % len_durations]
            else:
                next_split_point = durations[duration_index]
        except IndexError:
            break
        # grab next component from input stack of components
        try:
            x = xx.pop(0)
        except IndexError:
            break
        # find where end point of current component will position us
        next_cum_duration = cum_duration + x.prolated_duration
        #print x, duration_index, cum_duration, next_split_point
        # if current component fills duration of current part exactly
        if next_cum_duration == next_split_point:
            #print 'exactly equal %s' % x
            part.append(x)
            result.append(part)
            part = []
            cum_duration = durationtools.Duration(0)
            duration_index += 1
        # if current component exceeds duration of current part
        elif next_split_point < next_cum_duration:
            #print 'must split %s' % x
            local_split_duration = next_split_point - cum_duration
            #print cum_duration, next_split_point, x, part, local_split_duration
            left_list, right_list = _split_component_at_duration(x, local_split_duration,
                spanners = spanners, tie_after = tie_after)
            #print 'left_list, right_list %s, %s' % (left_list, right_list)
            part.extend(left_list)
            result.append(part)
            part = []
            # to avoid slice assignment pychecker errors
            #xx[0:0] = right_list
            xx.__setitem__(slice(0, 0), right_list)
            duration_index += 1
            cum_duration = durationtools.Duration(0)
        # if current component does not fill duration of current part
        else:
            #print 'simple append %s' % x
            part.append(x)
            cum_duration += x.prolated_duration
        #print ''

    # append stub part, if any
    if len(part):
        result.append(part)

    # append unexamined components, if any
    if len(xx):
        result.append(xx)

    # return list of parts, each of which is a list of components
    return result
