# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import mutate
Selection = selectiontools.Selection


def _rewrite_meter(
    components,
    meter,
    boundary_depth=None,
    maximum_dot_count=None,
    ):
    from abjad.tools import timesignaturetools

    assert isinstance(components, selectiontools.ContiguousSelection), \
        repr(components)

    def get_offsets_at_depth(depth):
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in \
                sequencetools.iterate_sequence_pairwise_strict(old_offsets):
                new_offsets.append(first)
                new_offsets.append((first + second) / 2)
            new_offsets.append(old_offsets[-1])
            offset_inventory.append(tuple(new_offsets))
        return offset_inventory[depth]

    def is_acceptable_tie_chain(tie_chain_duration,
        tie_chain_starts_in_offsets,
        tie_chain_stops_in_offsets):
        #print '\tTESTING ACCEPTABILITY'
        if not tie_chain_duration.is_assignable:
            return False
        if maximum_dot_count is not None and \
            maximum_dot_count < tie_chain_duration.dot_count:
            return False
        if not tie_chain_starts_in_offsets and not tie_chain_stops_in_offsets:
            return False
        return True

    def is_boundary_crossing_tie_chain(
        tie_chain_start_offset, tie_chain_stop_offset):
        #print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(tie_chain_start_offset < x < tie_chain_stop_offset 
            for x in boundary_offsets):
            return False
        if tie_chain_start_offset in boundary_offsets and \
            tie_chain_stop_offset in boundary_offsets:
            return False
        return True

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        #print 'DEPTH:', depth

        tie_chain_duration = tie_chain._preprolated_duration
        tie_chain_start_offset = tie_chain.get_timespan().start_offset
        tie_chain_stop_offset = tie_chain.get_timespan().stop_offset
        tie_chain_starts_in_offsets = tie_chain_start_offset in offsets
        tie_chain_stops_in_offsets = tie_chain_stop_offset in offsets

        if not is_acceptable_tie_chain(
            tie_chain_duration,
            tie_chain_starts_in_offsets,
            tie_chain_stops_in_offsets):

            #print 'UNACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            split_offset = None
            offsets = get_offsets_at_depth(depth)

            # If the tie chain's start aligns, take the latest possible offset.
            if tie_chain_starts_in_offsets:
                offsets = reversed(offsets)

            for offset in offsets:
                if tie_chain_start_offset < offset < tie_chain_stop_offset:
                    split_offset = offset
                    break

            #print '\tABS:', split_offset
            if split_offset is not None:
                split_offset -= tie_chain_start_offset
                #print '\tREL:', split_offset
                #print ''
                shards = mutate(tie_chain[:]).split([split_offset])
                tie_chains = \
                    [selectiontools.TieChain(shard) for shard in shards]
                for tie_chain in tie_chains:
                    recurse(tie_chain, depth=depth)
            else:
                #print ''
                recurse(tie_chain, depth=depth+1)

        elif is_boundary_crossing_tie_chain(
            tie_chain_start_offset,
            tie_chain_stop_offset):

            #print 'BOUNDARY CROSSING', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            offsets = boundary_offsets
            if tie_chain_start_offset in boundary_offsets:
                offsets = reversed(boundary_offsets)
            split_offset = None
            for offset in offsets:
                if tie_chain_start_offset < offset < tie_chain_stop_offset:
                    split_offset = offset
                    break
            assert split_offset is not None
            #print '\tABS:', split_offset
            split_offset -= tie_chain_start_offset
            #print '\tREL:', split_offset
            #print ''
            shards = mutate(tie_chain[:]).split([split_offset])
            tie_chains = \
                [selectiontools.TieChain(shard) for shard in shards]
            for tie_chain in tie_chains:
                recurse(tie_chain, depth=depth)

        else:
            #print 'ACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            #print ''
            tie_chain[:]._fuse()

    # Validate arguments.
    assert Selection._all_are_contiguous_components_in_same_logical_voice(
        components)
    if not isinstance(meter,
        timesignaturetools.Meter):
        meter = \
            timesignaturetools.Meter(meter)
    assert sum([x._preprolated_duration for x in components]) == \
        meter.preprolated_duration
    if boundary_depth is not None:
        boundary_depth = int(boundary_depth)
    if maximum_dot_count is not None:
        maximum_dot_count = int(maximum_dot_count)
        assert 0 <= maximum_dot_count

    # Build offset inventory, adjusted for initial offset and prolation.
    first_offset = components[0]._get_timespan().start_offset
    prolation = components[0]._get_parentage(include_self=False).prolation
    offset_inventory= []
    for offsets in meter.depthwise_offset_inventory:
        offsets = [(x * prolation) + first_offset for x in offsets]
        offset_inventory.append(tuple(offsets))

    # Build boundary offset inventory, if applicable.
    if boundary_depth is not None:
        boundary_offsets = offset_inventory[boundary_depth]

    # Cache results of iterator, as we'll be mutating the underlying collection.
    items = tuple(_iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(components))
    for item in items:
        if isinstance(item, selectiontools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            preprolated_duration = sum([x._preprolated_duration for x in item])
            if preprolated_duration.numerator == 1:
                preprolated_duration = mathtools.NonreducedFraction(
                    preprolated_duration)
                preprolated_duration = preprolated_duration.with_denominator(
                    preprolated_duration.denominator * 4)
            sub_metrical_hierarchy = timesignaturetools.Meter(preprolated_duration)
            sub_boundary_depth = 1
            if boundary_depth is None:
                sub_boundary_depth = None
            _rewrite_meter(
                item[:],
                sub_metrical_hierarchy,
                boundary_depth=sub_boundary_depth,
                maximum_dot_count=maximum_dot_count,
                )
   

def _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
    expr):
    r'''Iterate topmost masked tie chains, rest groups and containers in
    `expr`, masked by `expr`:

    ::

        >>> input = "abj: | 2/4 c'4 d'4 ~ |"
        >>> input += "| 4/4 d'8. r16 r8. e'16 ~ 2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ |"
        >>> input += "| 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ |"
        >>> input += "| 2/4 b'4 c''4 |"
        >>> staff = Staff(input)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            {
                \time 2/4
                c'4
                d'4 ~
            }
            {
                \time 4/4
                d'8.
                r16
                r8.
                e'16 ~
                \times 2/3 {
                    e'8 ~
                    e'8
                    f'8 ~
                }
                f'4 ~
            }
            {
                f'8
                g'8 ~
                g'4
                a'4 ~
                a'8
                b'8 ~
            }
            {
                \time 2/4
                b'4
                c''4
            }
        }

    ::

        >>> from abjad.tools.timesignaturetools._rewrite_meter \
        ...     import _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[0]): x
        ...
        TieChain(Note("c'4"),)
        TieChain(Note("d'4"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[1]): x
        ...
        TieChain(Note("d'8."),)
        TieChain(Rest('r16'), Rest('r8.'))
        TieChain(Note("e'16"),)
        Tuplet(2/3, [e'8, e'8, f'8])
        TieChain(Note("f'4"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[2]): x
        ...
        TieChain(Note("f'8"),)
        TieChain(Note("g'8"), Note("g'4"))
        TieChain(Note("a'4"), Note("a'8"))
        TieChain(Note("b'8"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[3]): x
        ...
        TieChain(Note("b'4"),)
        TieChain(Note("c''4"),)

    Returns generator.
    '''
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import selectiontools
    from abjad.tools import scoretools
    from abjad.tools import spannertools

    last_tie_spanner = None
    current_leaf_group = None
    current_leaf_group_is_silent = False

    for x in expr:
        if isinstance(x, (scoretools.Note, scoretools.Chord)):
            this_tie_spanner = x._get_spanners(spannertools.TieSpanner) or None
            if current_leaf_group is None:
                current_leaf_group = []
            elif current_leaf_group_is_silent or \
                this_tie_spanner is None or \
                last_tie_spanner != this_tie_spanner:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = False
            current_leaf_group.append(x)
            last_tie_spanner = this_tie_spanner
        elif isinstance(x, (scoretools.Rest, scoretools.Skip)):
            if current_leaf_group is None:
                current_leaf_group = []
            elif not current_leaf_group_is_silent:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = True
            current_leaf_group.append(x)
            last_tie_spanner = None
        elif isinstance(x, scoretools.Container):
            if current_leaf_group is not None:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = None
                last_tie_spanner = None
            yield x

        else:
            raise Exception('unhandled component found {!r}', x)
    if current_leaf_group is not None:
        yield selectiontools.TieChain(current_leaf_group)
