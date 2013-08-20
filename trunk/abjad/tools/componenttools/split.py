# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools


# TODO: fix bug that unintentionally fractures ties.
# TODO: add tests of tupletted notes and rests.
# TODO: add examples that show mark and context mark handling.
# TODO: add example showing grace and after grace handling.
def split(
    components, 
    durations,
    fracture_spanners=False, 
    cyclic=False, 
    tie_split_notes=True, 
    ):
    r'''Split `components` by `durations`.
    
    ..  container:: example

        **Example 1.** Split leaves:

        ::

            >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
            >>> leaves = staff.select_leaves()
            >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'8
                d'8
                f'8
                c'8
                e'8
                d'8
                f'8 \f
            }

        ::

            >>> durations = [Duration(3, 16), Duration(7, 32)]
            >>> result = componenttools.split(
            ...     leaves,
            ...     durations, 
            ...     tie_split_notes=False,
            ...     )
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'16 
                e'16
                d'8
                f'32 
                f'16.
                c'8
                e'8
                d'8
                f'8 \f
            }

    ..  container:: example

        **Example 2.** Split leaves and fracture crossing spanners:

        ::

            >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
            >>> leaves = staff.select_leaves()
            >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'8
                d'8
                f'8
                c'8
                e'8
                d'8
                f'8 \f
            }

        ::

            >>> durations = [Duration(3, 16), Duration(7, 32)]
            >>> result = componenttools.split(
            ...     leaves,
            ...     durations, 
            ...     fracture_spanners=True, 
            ...     tie_split_notes=False,
            ...     )
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'16 \f 
                e'16 \< \p
                d'8
                f'32 \f 
                f'16. \< \p
                c'8
                e'8
                d'8
                f'8 \f
            }

    ..  container:: example

        **Example 3.** Split leaves cyclically:

        ::

            >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
            >>> leaves = staff.select_leaves()
            >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'8
                d'8
                f'8
                c'8
                e'8
                d'8
                f'8 \f
            }

        ::

            >>> durations = [Duration(3, 16), Duration(7, 32)]
            >>> result = componenttools.split(
            ...     leaves,
            ...     durations,
            ...     cyclic=True,
            ...     tie_split_notes=False,
            ...     )
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'16 
                e'16
                d'8
                f'32 
                f'16.
                c'16. 
                c'32
                e'8
                d'16 
                d'16
                f'8 \f
            }

    ..  container:: example

        **Example 4.** Split leaves cyclically and fracture spanners:

        ::

            >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
            >>> leaves = staff.select_leaves()
            >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
            >>> staff.override.dynamic_line_spanner.staff_padding = 3
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'8
                d'8
                f'8
                c'8
                e'8
                d'8
                f'8 \f
            }

        ::

            >>> durations = [Duration(3, 16), Duration(7, 32)]
            >>> result = componenttools.split(
            ...     leaves,
            ...     durations,
            ...     cyclic=True, 
            ...     fracture_spanners=True,
            ...     tie_split_notes=False,
            ...     )
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override DynamicLineSpanner #'staff-padding = #3
            } {
                c'8 \< \p
                e'16 \f 
                e'16 \< \p
                d'8
                f'32 \f 
                f'16. \< \p
                c'16. \f 
                c'32 \< \p
                e'8
                d'16 \f 
                d'16 \< \p
                f'8 \f
            }

    ..  container:: example

        **Example 5.** Split tupletted leaves and fracture crossing spanners:

        ::

            >>> staff = Staff()
            >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
            >>> leaves = staff.select_leaves()
            >>> spanner = spannertools.SlurSpanner(leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4 (
                    d'4
                    e'4
                }
                \times 2/3 {
                    c'4
                    d'4
                    e'4 )
                }
            }

        ::

            >>> durations = [Duration(1, 4)]
            >>> result = componenttools.split(
            ...     leaves,
            ...     durations, 
            ...     fracture_spanners=True, 
            ...     tie_split_notes=False,
            ...     )
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4 (
                    d'8 ) 
                    d'8 (
                    e'4
                }
                \times 2/3 {
                    c'4
                    d'4
                    e'4 )
                }
            }

    Return list of lists.
    '''
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    from abjad.tools import selectiontools

    # check input
    assert all(isinstance(x, componenttools.Component) for x in components)
    if not isinstance(components, selectiontools.SliceSelection):
        components = selectiontools.SliceSelection(components)
    durations = [durationtools.Duration(x) for x in durations]

    if not durations:
        return [], components

    # calculate total component duration
    total_component_duration = components.get_duration()
    total_split_duration = sum(durations)

    # calculate durations
    if cyclic:
        durations = sequencetools.repeat_sequence_to_weight_exactly(
            durations, total_component_duration)
    elif total_split_duration < total_component_duration:
        final_offset = total_component_duration - sum(durations)
        durations.append(final_offset)
    elif total_component_duration < total_split_duration:
        durations = sequencetools.truncate_sequence_to_weight(
            durations, total_component_duration)

    #print durations, 'durations'

    # keep copy of durations to partition result components
    durations_copy = durations[:]

    # calculate total offset duration
    total_split_duration = sum(durations)
    assert total_split_duration == total_component_duration

    # initialize loop variables
    result, shard = [], []
    offset_index, offset_count = 0, len(durations)
    current_shard_duration = durationtools.Duration(0)
    remaining_components = list(components[:])
    advance_to_next_offset = True

    # loop and build shards by grabbing next component and next offset 
    # each time through loop
    while True:

        # grab next split point
        if advance_to_next_offset:
            if durations:
                #print durations
                next_split_point = durations.pop(0)
                #print next_split_point
            else:
                #print 'no more durations'
                break

        advance_to_next_offset = True

        # grab next component from input stack of components
        if remaining_components:
            current_component = remaining_components.pop(0)
        else:
            #print 'no more components'
            break

        # find where current component endpoint will position us
        candidate_shard_duration = current_shard_duration + \
            current_component._get_duration()

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

            if isinstance(current_component, leaftools.Leaf):
                #print 'splitting leaf ...'
                leaf_split_durations = [local_split_duration]
                additional_required_duration = \
                    current_component._get_duration() - local_split_duration
                #print 'durations {}'.format(durations)
                split_durations = sequencetools.split_sequence_by_weights(
                    durations, 
                    [additional_required_duration], 
                    cyclic=False, 
                    overhang=True,
                    )
                #print 'split_durations {}\n'.format(split_durations)
                additional_durations = split_durations[0]
                leaf_split_durations.extend(additional_durations)
                durations = split_durations[-1]
                leaf_shards = current_component._split_by_durations(
                    leaf_split_durations,
                    cyclic=False, 
                    fracture_spanners=fracture_spanners,
                    tie_split_notes=tie_split_notes,
                    )
                shard.extend(leaf_shards)
                result.append(shard)
                offset_index += len(additional_durations)
            else:
                #print 'splitting container ...'
                left_list, right_list = \
                    componenttools.split_component_by_duration(
                    current_component, 
                    local_split_duration, 
                    fracture_spanners=fracture_spanners,
                    tie_split_notes=tie_split_notes, 
                    )
                shard.extend(left_list)
                result.append(shard)
                remaining_components.__setitem__(slice(0, 0), right_list)

            shard = []
            offset_index += 1
            current_shard_duration = durationtools.Duration(0)
        # if current component would not fill current shard
        elif candidate_shard_duration < next_split_point:
            #print 'simple append %s' % current_component
            shard.append(current_component)
            current_shard_duration += current_component._get_duration()
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
    result = selectiontools.ContiguousSelection(result)
    result = result.partition_by_durations_exactly(durations_copy)

    # return list of shards
    return result
