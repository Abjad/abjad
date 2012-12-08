from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import sequencetools
from abjad.tools import tietools


def establish_metrical_hierarchy(components, metrical_hierarchy, maximum_dot_count=None):
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

    def is_acceptable_tie_chain(tie_chain, offsets):
        if tie_chain.preprolated_duration.is_assignable:
            if maximum_dot_count is not None and \
                maximum_dot_count < tie_chain.preprolated_duration.dot_count:
                return False
            if tie_chain.start_offset in offsets:
                return True
            if tie_chain.stop_offset in offsets:
                return True
        return False

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        #print 'DEPTH:', depth

        if is_acceptable_tie_chain(tie_chain, offsets):
            #print 'ACCEPTABLE:', tie_chain, tie_chain.start_offset, tie_chain.stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            #print ''
            leaftools.fuse_leaves(tie_chain[:])

        else:
            #print 'UNACCEPTABLE:', tie_chain, tie_chain.start_offset, tie_chain.stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            split_offset = None
            offsets = get_offsets_at_depth(depth)

            # if the tie chain's start aligns, take the latest possible offset
            if tie_chain.start_offset in offsets:
                offsets = reversed(offsets)

            for offset in offsets:
                if tie_chain.start_offset < offset < tie_chain.stop_offset:
                    split_offset = offset
                    break

            #print '\tABS:', split_offset
            if split_offset is not None:
                split_offset -= tie_chain.start_offset
                #print '\tREL:', split_offset
                #print ''
                tie_chains = [tietools.TieChain(shard) for shard in
                    componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
                for tie_chain in tie_chains:
                    recurse(tie_chain, depth=depth)

            else:
                #print ''
                recurse(tie_chain, depth=depth+1)

    # cache results of iterator, as we'll be mutating the underlying collection
    items = tuple(tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(components))
    for item in items:
        #print ''
        if isinstance(item, tietools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            duration = sum([x.preprolated_duration for x in item])
            sub_metrical_hierarchy = timesignaturetools.MetricalHierarchy(duration)
            establish_metrical_hierarchy(item[:], sub_metrical_hierarchy)
