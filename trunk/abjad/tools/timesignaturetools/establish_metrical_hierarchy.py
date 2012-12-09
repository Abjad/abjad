from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import sequencetools
from abjad.tools import tietools


def establish_metrical_hierarchy(components, metrical_hierarchy,
    maximum_dot_count=None,
    show_boundaries=False,
    ):
    r'''.. versionadded:: 2.11

    Operate in place and return none.
    '''

    from abjad.tools import timesignaturetools

    assert componenttools.all_are_thread_contiguous_components(components)
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(metrical_hierarchy)
    assert sum([x.preprolated_duration for x in components]) == metrical_hierarchy.duration
    if maximum_dot_count is not None:
        maximum_dot_count = int(maximum_dot_count)
        assert 0 <= maximum_dot_count

    first_offset = components[0].start_offset
    prolation = components[0].prolation

    offset_inventory= []
    for offsets in metrical_hierarchy.depthwise_offset_inventory:
        offsets = [(x * prolation) + first_offset for x in offsets]
        offset_inventory.append(tuple(offsets))
    boundary_offsets = offset_inventory[-1]

    def get_offsets_at_depth(depth):
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth: 
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in sequencetools.iterate_sequence_pairwise_strict(old_offsets):
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

    def is_boundary_crossing_tie_chain(tie_chain_start_offset, tie_chain_stop_offset):
        #print '\tTESTING BOUNDARY CROSSINGS'
        if not show_boundaries:
            return False
        if not any(tie_chain_start_offset < x < tie_chain_stop_offset for x in boundary_offsets):
            return False
        if tie_chain_start_offset in boundary_offsets and tie_chain_stop_offset in boundary_offsets:
            return False
        return True

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        #print 'DEPTH:', depth

        tie_chain_duration = tie_chain.preprolated_duration
        tie_chain_start_offset = tie_chain.start_offset
        tie_chain_stop_offset = tie_chain.stop_offset
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

            # if the tie chain's start aligns, take the latest possible offset
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
                tie_chains = [tietools.TieChain(shard) for shard in
                    componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
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
            tie_chains = [tietools.TieChain(shard) for shard in
                componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
            for tie_chain in tie_chains:
                recurse(tie_chain, depth=depth)

        else:
            #print 'ACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            #print ''
            leaftools.fuse_leaves(tie_chain[:])


    # cache results of iterator, as we'll be mutating the underlying collection
    items = tuple(tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(components))
    for item in items:
        ##print ''
        if isinstance(item, tietools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            duration = sum([x.preprolated_duration for x in item])
            sub_metrical_hierarchy = timesignaturetools.MetricalHierarchy(duration)
            establish_metrical_hierarchy(item[:], sub_metrical_hierarchy)
