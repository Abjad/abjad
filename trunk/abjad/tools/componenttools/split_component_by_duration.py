# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools


def split_component_by_duration(
    component,
    offset,
    fracture_spanners=False,
    tie_split_notes=True,
    tie_split_rests=False,
    ):
    r'''Split `component` at `offset`.

    ..  container:: example

        **Example 1.** Split `component` at `offset`. Don't fracture spanners:

        ::

            >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
            >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

        ::

            >>> spannertools.BeamSpanner(staff[0])
            BeamSpanner(|2/8(2)|)
            >>> spannertools.BeamSpanner(staff[1])
            BeamSpanner(|2/8(2)|)
            >>> spannertools.SlurSpanner(staff.select_leaves())
            SlurSpanner(c'8, d'8, e'8, f'8)

        ..  doctest::

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

            >>> show(staff) # doctest: +SKIP

        ::

            >>> halves = componenttools.split_component_by_duration(
            ... staff.select_leaves()[0], (1, 32), fracture_spanners=False, tie_split_notes=False)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'32 [ (
                    c'16.
                    d'8 ]
                }
                {
                    e'8 [
                    f'8 ] )
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Split component at offset at fracture crossing spanners:

        ::

            >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
            >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

        ::

            >>> spannertools.BeamSpanner(staff[0])
            BeamSpanner(|2/8(2)|)
            >>> spannertools.BeamSpanner(staff[1])
            BeamSpanner(|2/8(2)|)
            >>> spannertools.SlurSpanner(staff.select_leaves())
            SlurSpanner(c'8, d'8, e'8, f'8)

        ..  doctest::

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

            >>> show(staff) # doctest: +SKIP

        ::

            >>> halves = componenttools.split_component_by_duration(
            ... staff.select_leaves()[0], (1, 32), fracture_spanners=True, tie_split_notes=False)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'32 [ ( )
                    c'16. (
                    d'8 ]
                }
                {
                    e'8 [
                    f'8 ] )
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    Return pair of left and right part-lists.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import measuretools
    from abjad.tools import notetools
    from abjad.tools import resttools
    from abjad.tools import selectiontools
    from abjad.tools import spannertools

    # check input
    assert isinstance(component, componenttools.Component)
    offset = durationtools.Offset(offset)
    assert 0 <= offset, repr(offset)

    # if zero offset then return empty list and component
    if offset == 0:
        return [], component

    if isinstance(component, leaftools.Leaf):
        return component._split_at_offset(
            offset,
            fracture_spanners=fracture_spanners,
            tie_split_notes=tie_split_notes,
            tie_split_rests=tie_split_rests,
            )

    # get split point score offset
    global_split_point = component._get_timespan().start_offset + offset

    # get any duration-crossing descendents
    cross_offset = component._get_timespan().start_offset + offset
    duration_crossing_descendants = []
    for descendant in component._select_descendants():
        start_offset = descendant._get_timespan().start_offset
        stop_offset = descendant._get_timespan().stop_offset
        if start_offset < cross_offset < stop_offset:
            duration_crossing_descendants.append(descendant)

    # get any duration-crossing measure descendents
    measures = [
        x for x in duration_crossing_descendants 
        if isinstance(x, measuretools.Measure)
        ]

    # if we must split a power-of-two measure at non-power-of-two split point
    # go ahead and transform the power-of-two measure to non-power-of-two 
    # equivalent now; code that crawls and splits later on will be happier
    if len(measures) == 1:
        measure = measures[0]
        split_point_in_measure = \
            global_split_point - measure._get_timespan().start_offset
        if measure.has_non_power_of_two_denominator:
            if not measure.implied_prolation ==\
                split_point_in_measure.implied_prolation:
                raise NotImplementedError
        elif not mathtools.is_nonnegative_integer_power_of_two(
            split_point_in_measure.denominator):
            non_power_of_two_factors = mathtools.remove_powers_of_two(
                split_point_in_measure.denominator)
            non_power_of_two_factors = mathtools.factors(
                non_power_of_two_factors)
            non_power_of_two_product = 1
            for non_power_of_two_factor in non_power_of_two_factors:
                non_power_of_two_product *= non_power_of_two_factor
            measuretools.scale_measure_denominator_and_adjust_measure_contents(
                measure, non_power_of_two_product)
            # rederive duration crosses with possibly new measure contents
            cross_offset = component._get_timespan().start_offset + offset
            duration_crossing_descendants = []
            for descendant in component._select_descendants():
                start_offset = descendant._get_timespan().start_offset
                stop_offset = descendant._get_timespan().stop_offset
                if start_offset < cross_offset < stop_offset:
                    duration_crossing_descendants.append(descendant)
    elif 1 < len(measures):
        raise Exception('measures can not nest.')

    # any duration-crossing leaf will be at end of list
    bottom = duration_crossing_descendants[-1]

    did_split_leaf = False

    # if split point necessitates leaf split
    if isinstance(bottom, leaftools.Leaf):
        assert isinstance(bottom, leaftools.Leaf)
        did_split_leaf = True
        split_point_in_bottom = \
            global_split_point - bottom._get_timespan().start_offset
        left_list, right_list = bottom._split_at_offset(
            split_point_in_bottom,
            fracture_spanners=fracture_spanners,
            tie_split_notes=tie_split_notes,
            tie_split_rests=tie_split_rests,
            )
        right = right_list[0]
        leaf_right_of_split = right
        leaf_left_of_split = left_list[-1]
        duration_crossing_containers = duration_crossing_descendants[:-1]
        if not len(duration_crossing_containers):
            return left_list, right_list
    # if split point falls between leaves
    # then find leaf to immediate right of split point
    # in order to start upward crawl through duration-crossing containers
    else:
        duration_crossing_containers = duration_crossing_descendants[:]
        for leaf in iterationtools.iterate_leaves_in_expr(bottom):
            if leaf._get_timespan().start_offset == global_split_point:
                leaf_right_of_split = leaf
                leaf_left_of_split = \
                    leaftools.get_nth_leaf_in_logical_voice_from_leaf(
                    leaf_right_of_split, -1)
                break
        else:
            message = 'can not split empty container {!r}.'
            raise ContainmentError(message.format(bottom))

    # find component to right of split that is also immediate child of 
    # last duration-crossing container
    for component in leaf_right_of_split._select_parentage(include_self=True):
        if component._parent is duration_crossing_containers[-1]:
            highest_level_component_right_of_split = component
            break
    else:
        raise ValueError('should we be able to get here?')

    # crawl back up through duration-crossing containers and 
    # fracture spanners if requested
    if fracture_spanners:
        start_offset = leaf_right_of_split._get_timespan().start_offset
        for parent in leaf_right_of_split._select_parentage():
            if parent._get_timespan().start_offset == start_offset:
                spannertools.fracture_spanners_attached_to_component(
                    parent, direction=Left)
            if parent is component:
                break

    # crawl back up through duration-crossing containers and split each
    prev = highest_level_component_right_of_split
    for duration_crossing_container in reversed(duration_crossing_containers):
        assert isinstance(
            duration_crossing_container, containertools.Container)
        i = duration_crossing_container.index(prev)
        left, right = containertools.split_container_at_index(
            duration_crossing_container,
            i,
            fracture_spanners=fracture_spanners,
            )
        prev = right

    # NOTE: If tie chain here is convenience, then fusing is good.
    #       If tie chain here is user-given, then fusing is less good.
    #       Maybe later model difference between user tie chains and not.
    left_tie_chain = leaf_left_of_split._select_tie_chain()
    right_tie_chain = leaf_right_of_split._select_tie_chain()
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(left_tie_chain)
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(right_tie_chain)

    # reapply tie here if crawl above killed tie applied to leaves
    if did_split_leaf:
        if  (tie_split_notes and isinstance(leaf_left_of_split, notetools.Note)) or \
            (tie_split_rests and isinstance(leaf_left_of_split, resttools.Rest)):
            if leaf_left_of_split._select_parentage().root is \
                leaf_right_of_split._select_parentage().root:
                leaves_around_split = (leaf_left_of_split, leaf_right_of_split)
                selection = selectiontools.ContiguousLeafSelection(
                    leaves_around_split)
                selection._attach_tie_spanner_to_leaf_pair()

    # return pair of left and right list-wrapped halves of container
    return ([left], [right])
