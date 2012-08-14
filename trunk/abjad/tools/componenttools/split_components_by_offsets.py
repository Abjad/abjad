from abjad.tools.componenttools.split_component_at_offset import split_component_at_offset
from abjad.tools import durationtools


# TODO: fix bug that unintentionally fractures ties.
def split_components_by_offsets(components, durations,
    fracture_spanners=False, cyclic=False, tie_after=False):
    r'''.. versionadded:: 2.0
    
    Example 1. Split components cyclically and do not fracture crossing spanners::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> componenttools.split_components_by_offsets(staff.leaves, [Duration(3, 32)], cyclic=True)
        [[Note("c'16.")], [Note("c'32"), Note("d'16")],
        [Note("d'16"), Note("e'32")], [Note("e'16.")], [Note("f'16.")], [Note("f'32")]]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16. [ (
                c'32
                d'16
                d'16 ]
            }
            {
                e'32 [
                e'16.
                f'16.
                f'32 ] )
            }
        }

    Example 2. Split components cyclically and fracture spanners::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> result = componenttools.split_components_by_offsets(
        ... staff.leaves, [Duration(3, 32)], cyclic=True, fracture_spanners=True)

    ::

        >>> result
        [[Note("c'16.")], [Note("c'32"), Note("d'16")], [Note("d'16"), Note("e'32")],
        [Note("e'16.")], [Note("f'16.")], [Note("f'32")]]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16. ( ) [
                c'32 (
                d'16 )
                d'16 ] (
            }
            {
                e'32 ) [
                e'16. (
                f'16. )
                f'32 ] ( )
            }
        }

    Example 3. Split components once and do not fracture crossing spanners::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]

    ::

        >>> parts = componenttools.split_components_by_offsets(
        ... staff[:1], durations, cyclic=False, fracture_spanners=False)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }

    Example 4. Split components once and fracture crossing spanners::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
        >>> parts = componenttools.split_components_by_offsets(
        ... staff[:1], durations, cyclic=False, fracture_spanners=True)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }

    Return list of newly split parts.
    '''
    from abjad.tools import componenttools

    # check input
    assert componenttools.all_are_components(components)
    assert durationtools.all_are_duration_tokens(durations)

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
            left_list, right_list = split_component_at_offset(x, local_split_duration,
                fracture_spanners=fracture_spanners, tie_after=tie_after)
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
