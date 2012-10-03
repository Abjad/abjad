from abjad.tools import durationtools
from abjad.tools import sequencetools


# TODO: fix bug that unintentionally fractures ties.
def split_components_at_offsets(components, offsets, 
    fracture_spanners=False, cyclic=False, tie_split_notes=True, tie_split_rests=False):
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

        >>> componenttools.split_components_at_offsets(
        ...     staff.leaves, [Duration(3, 32)], cyclic=True)
        [[Note("c'16.")], [Note("c'32"), Note("d'16")],
        [Note("d'16"), Note("e'32")], [Note("e'16.")], [Note("f'16.")], [Note("f'32")]]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16. [ ( ~
                c'32
                d'16 ~
                d'16 ]
            }
            {
                e'32 [ ~
                e'16.
                f'16. ~
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

        >>> result = componenttools.split_components_at_offsets(
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
                c'16. ( ) [ ~
                c'32 (
                d'16 ) ~
                d'16 ] (
            }
            {
                e'32 ) [ ~
                e'16. (
                f'16. ) ~
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

        >>> shards = componenttools.split_components_at_offsets(
        ... staff[:1], offsets, cyclic=False, fracture_spanners=False, tie_split_notes=False)

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
        >>> shards = componenttools.split_components_at_offsets(
        ... staff[:1], offsets, cyclic=False, fracture_spanners=True, tie_split_notes=False)

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

    Example 5. Split tupletted components once and fracture crossing spanners::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner({c'8, d'8, e'8})
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner({f'8, g'8, a'8})
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8, g'8, a'8)

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [ (
                d'8
                e'8 ]
            }
            \times 2/3 {
                f'8 [
                g'8
                a'8 ] )
            }
        }

    ::

        >>> offsets = [(1, 8)]
        >>> shards = componenttools.split_components_at_offsets(
        ... staff.leaves, offsets, cyclic=False, fracture_spanners=True, tie_split_notes=True)

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [ (
                d'16 ) ~
                d'16 (
                e'8 ]
            }
            \times 2/3 {
                f'8 [
                g'8
                a'8 ] )
            }
        }

    Return list of newly split shards.

    .. note:: Add tests of tupletted notes and rests.

    .. note:: Add examples that show mark and context mark handling.

    .. note:: Add example showing grace and after grace handling.
    '''
    from abjad.tools import componenttools
    from abjad.tools import leaftools

    # check input
    assert componenttools.all_are_components(components)
    offsets = [durationtools.Offset(offset) for offset in offsets]

    # calculate total component duration
    total_component_duration = componenttools.sum_prolated_duration_of_components(components)
    total_offset_duration = sum(offsets)

    # calculate offsets
    if cyclic:
        offsets = sequencetools.repeat_sequence_to_weight_exactly(offsets, total_component_duration)
    elif total_offset_duration < total_component_duration:
        final_offset = total_component_duration - sum(offsets)
        offsets.append(final_offset)
    elif total_component_duration < total_offset_duration:
        offsets = sequencetools.truncate_sequence_to_weight(offsets, total_component_duration)

    #print offsets, 'offsets'

    # keep copy of offsets to partition result components
    offsets_copy = offsets[:]
    
    # calculate total offset duration
    total_offset_duration = sum(offsets)
    assert total_offset_duration == total_component_duration

    # initialize loop variables
    result, shard = [], []
    offset_index, offset_count = 0, len(offsets)
    current_shard_duration = durationtools.Duration(0)
    remaining_components = list(components[:])
    advance_to_next_offset = True

    # loop and build shards by grabbing next component and next offset each time through loop
    while True:

        # grab next split point
        if advance_to_next_offset:
            if offsets:
                #print offsets
                next_split_point = offsets.pop(0)
                #print next_split_point
            else:
                #print 'no more offsets'
                break

        advance_to_next_offset = True

        # grab next component from input stack of components
        if remaining_components:
            current_component = remaining_components.pop(0)
        else:
            #print 'no more components'
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
            #print 'local_split_duration {}'.format(local_split_duration)
            #print current_shard_duration, next_split_point, current_component, shard, local_split_duration

            if isinstance(current_component, leaftools.Leaf):
                #print 'splitting leaf ...'
                leaf_split_durations = [local_split_duration]
                additional_required_duration = current_component.prolated_duration - local_split_duration
                #print 'additional_required_duration {}'.format(additional_required_duration)
                #print 'offsets {}'.format(offsets)
                split_offsets = sequencetools.split_sequence_by_weights(
                    offsets, [additional_required_duration], cyclic=False, overhang=True)
                #print 'split_offsets {}\n'.format(split_offsets)
                additional_offsets = split_offsets[0]
                leaf_split_durations.extend(additional_offsets)
                offsets = split_offsets[-1]
                leaf_shards = leaftools.split_leaf_at_offsets(
                    current_component, leaf_split_durations, 
                    cyclic=False, fracture_spanners=fracture_spanners)
                shard.extend(leaf_shards)
                result.append(shard)
                offset_index += len(additional_offsets)
            else:
                #print 'splitting container ...'
                left_list, right_list = componenttools.split_component_at_offset(
                    current_component, local_split_duration, fracture_spanners=fracture_spanners, 
                    tie_split_notes=tie_split_notes, tie_split_rests=tie_split_rests)
                #print 'left_list, right_list {}, {}'.format(left_list, right_list)
                shard.extend(left_list)
                result.append(shard)
                # to avoid slice assignment pychecker errors
                #remaining_components[0:0] = right_list
                remaining_components.__setitem__(slice(0, 0), right_list)

            shard = []
            offset_index += 1
            current_shard_duration = durationtools.Duration(0)
        # if current component would not fill current shard
        elif candidate_shard_duration < next_split_point:
            #print 'simple append %s' % current_component
            shard.append(current_component)
            current_shard_duration += current_component.prolated_duration
            advance_to_next_offset = False
        else:
            raise ValueError
        #print ''

    # append any stub shard
    if len(shard):
        result.append(shard)

    # append any unexamined components
    if len(remaining_components):
        result.append(remaining_components)

    # group split components according to input durations
    result = sequencetools.flatten_sequence(result)
    result = componenttools.partition_components_by_durations_exactly(result, offsets_copy)

    # return list of shards
    return result
