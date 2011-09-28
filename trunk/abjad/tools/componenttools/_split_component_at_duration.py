from abjad.exceptions import ContainmentError
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.componenttools._split_component_at_index import _split_component_at_index
from abjad.tools import durationtools


def _split_component_at_duration(component, duration, spanners='unfractured', tie_after=False):
    '''General component duration split algorithm.
    Duration is interpreted as prolated duration.
    Works on leaves, tuplets, measures, context and unqualified containers.
    Keyword controls spanner behavior at split-time.
    '''
    from abjad.tools.containertools.Container import Container
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools import leaftools
    from abjad.tools import measuretools
    from abjad.tools import spannertools
    from abjad.tools import tietools
    from abjad.tools.componenttools.list_improper_contents_of_component_that_cross_prolated_offset \
        import list_improper_contents_of_component_that_cross_prolated_offset
    from abjad.tools.leaftools._split_leaf_at_duration import _split_leaf_at_duration
    from abjad.tools.leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian \
        import fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
    from abjad.tools.measuretools.Measure import Measure

    duration = durationtools.Duration(duration)
    assert 0 <= duration

    # if zero duration then return component
    if duration == 0:
        # TODO: This one case should be ([], component) #
        return (component, )

    # get global position of duration split in score
    global_split_point = component._offset.start + duration

    # get duration crossers, if any
    contents = list_improper_contents_of_component_that_cross_prolated_offset(component, duration)

    #print component, global_split_point, contents

    # get duration crossing measures, if any
    measures = [x for x in contents if isinstance(x, Measure)]

    # if we must split a binary measure at a nonbinary split point
    # go ahead and transform the binary measure to nonbinary equiavlent now;
    # code that crawls and splits later on will be happier
    if len(measures) == 1:
        measure = measures[0]
        split_point_in_measure = global_split_point - measure._offset.start
        split_point_denominator = split_point_in_measure.denominator
        if measure.is_nonbinary:
            measure_multiplier = measure.multiplier
            split_point_multiplier = durationtools.positive_integer_to_implied_prolation_multipler(
                split_point_denominator)
            if not measure_multiplier == split_point_multiplier:
                raise NotImplementedError
        elif not mathtools.is_nonnegative_integer_power_of_two(split_point_denominator):
            nonbinary_factors = mathtools.factors(
                mathtools.remove_powers_of_two(split_point_denominator))
            nonbinary_product = 1
            for nonbinary_factor in nonbinary_factors:
                nonbinary_product *= nonbinary_factor
            measuretools.scale_measure_denominator_and_adjust_measure_contents(
                measure, nonbinary_product)
            # rederive duration crosses with possibly new measure contents
            contents = list_improper_contents_of_component_that_cross_prolated_offset(
                component, duration)
    elif 1 < len(measures):
        raise ContainmentError('measures can not nest.')

    # if leaf duration crosser, will be at end of list
    bottom = contents[-1]

    did_split_leaf = False

    # if split point necessitates leaf split
    if isinstance(bottom, _Leaf):
        assert isinstance(bottom, _Leaf)
        did_split_leaf = True
        split_point_in_bottom = global_split_point - bottom._offset.start
        left_list, right_list = _split_leaf_at_duration(bottom,
            split_point_in_bottom, spanners = spanners, tie_after = tie_after)
        right = right_list[0]
        leaf_right_of_split = right
        leaf_left_of_split = left_list[-1]
        containers = contents[:-1]
        if not len(containers):
            return left_list, right_list
    # if split point falls between leaves
    # then find leaf to immediate right of split point
    # in order to start upward crawl through containers
    else:
        containers = contents[:]
        for leaf in leaftools.iterate_leaves_forward_in_expr(bottom):
            if leaf._offset.start == global_split_point:
                right = leaf
                leaf_right_of_split = right
                leaf_left_of_split = right._navigator._prev_bead
                break
        else:
            raise ContainmentError('can not split empty container.')

    # fracture leaf spanners if requested
    if spanners == 'fractured':
        #right.spanners.fracture(direction = 'left')
        spannertools.fracture_all_spanners_attached_to_component(right, direction = 'left')

    # crawl back up through container duration crossers
    # split each container duration crosser
    for cur in reversed(containers):
        assert isinstance(cur, Container)
        prev = right
        i = cur.index(prev)
        left, right = _split_component_at_index(cur, i, spanners = spanners)

    # NOTE: If tie chain here is convenience, then fusing is good.
    #         If tie chain here is user-given, then fusing is less good.
    #         Maybe later model difference between user tie chains and not.
    fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
        tietools.get_tie_chain(leaf_left_of_split))
    fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
        tietools.get_tie_chain(leaf_right_of_split))

    # crawl above will kill any tie applied to leaves
    # reapply tie here if necessary
    # TODO: Possibly replace this with tietools.apply_tie_spanner_to_leaf_pair()? #
    if did_split_leaf:
        if tie_after:
            leaves_at_split = [leaf_left_of_split, leaf_right_of_split]
            if not tietools.are_components_in_same_tie_spanner(leaves_at_split):
                #if all([x.tie.spanned for x in leaves_at_split]):
                if all([tietools.is_component_with_tie_spanner_attached(x) for x in leaves_at_split]):
                    #leaf_left_of_split.tie.spanner.fuse(leaf_right_of_split.tie.spanner)
                    leaf_left_of_split_tie_spanner = \
                        spannertools.get_the_only_spanner_attached_to_component(
                        leaf_left_of_split, tietools.TieSpanner)
                    leaf_right_of_split_tie_spanner = \
                        spannertools.get_the_only_spanner_attached_to_component(
                        leaf_right_of_split, tietools.TieSpanner)
                    leaf_left_of_split_tie_spanner.fuse(leaf_right_of_split_tie_spanner)
                else:
                    tietools.TieSpanner(leaves_at_split)

    # return pair of left and right list-wrapped halves of container
    return ([left], [right])
