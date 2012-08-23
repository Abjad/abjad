from abjad.tools import durationtools


# TODO: fix bug that unintentionally fractures ties.
def split_components_by_offsets(components, offsets, fracture_spanners=False, cyclic=False, tie_after=False):
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

        >>> componenttools.split_components_by_offsets(
        ...     staff.leaves, [Duration(3, 32)], cyclic=True)
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

        >>> offsets = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]

    ::

        >>> shards = componenttools.split_components_by_offsets(
        ... staff[:1], offsets, cyclic=False, fracture_spanners=False)

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

        >>> offsets = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
        >>> shards = componenttools.split_components_by_offsets(
        ... staff[:1], offsets, cyclic=False, fracture_spanners=True)

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

    Return list of newly split shards.
    '''
    from abjad.tools import componenttools

    # check input
    assert componenttools.all_are_components(components)
    assert durationtools.all_are_duration_tokens(offsets)

    # initialize loop variables
    result, shard = [], []
    offset_index, offset_count = 0, len(offsets)
    current_shard_duration = durationtools.Duration(0)
    remaining_components = list(components[:])

    # loop and build shards
    # grab next component and next offset each time through loop
    while True:
        #print 'remaining_components are now %s' % remaining_components

        # grab next split point
        if cyclic:
            next_split_point = offsets[offset_index % offset_count]
        elif offset_index < offset_count:
            next_split_point = offsets[offset_index]
        else:
            break

        # grab next component from input stack of components
        if remaining_components:
            current_component = remaining_components.pop(0)
        else:
            break

        # find where current component endpoint will position us
        candidate_shard_duration = current_shard_duration + current_component.prolated_duration
        #print current_component, offset_index, current_shard_duration, next_split_point

        # if current component would fill current shard exactly
        if candidate_shard_duration == next_split_point:
            #print 'exactly equal %s' % current_component
            shard.append(current_component)
            result.append(shard)
            shard = []
            current_shard_duration = durationtools.Duration(0)
            offset_index += 1
        # if current component would exceed current shard
        elif next_split_point < candidate_shard_duration:
            #print 'must split %s' % current_component
            local_split_duration = next_split_point - current_shard_duration
            #print current_shard_duration, next_split_point, current_component, shard, local_split_duration
            left_list, right_list = componenttools.split_component_at_offset(
                current_component, local_split_duration, fracture_spanners=fracture_spanners, tie_after=tie_after)
            #print 'left_list, right_list %s, %s' % (left_list, right_list)
            shard.extend(left_list)
            result.append(shard)
            shard = []
            # to avoid slice assignment pychecker errors
            #remaining_components[0:0] = right_list
            remaining_components.__setitem__(slice(0, 0), right_list)
            offset_index += 1
            current_shard_duration = durationtools.Duration(0)
        # if current component would not fill current shard
        elif candidate_shard_duration < next_split_point:
            #print 'simple append %s' % current_component
            shard.append(current_component)
            current_shard_duration += current_component.prolated_duration
        else:
            raise ValueError
        #print ''

    # append any stub shard
    if len(shard):
        result.append(shard)

    # append any unexamined components
    if len(remaining_components):
        result.append(remaining_components)

    # return list of shards
    return result
