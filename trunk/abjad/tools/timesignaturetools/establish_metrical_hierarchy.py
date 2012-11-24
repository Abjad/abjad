from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import sequencetools
from abjad.tools import tietools


def establish_metrical_hierarchy(components, metrical_hierarchy):
    r'''.. versionadded:: 2.11

    Operate in place and return none.
    '''

    from abjad.tools import timesignaturetools

    assert componenttools.all_are_thread_contiguous_components(components)
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(metrical_hierarchy)
    assert sum([x.preprolated_duration for x in components]) == metrical_hierarchy.duration

    first_offset = components[0].start_offset
    prolation = components[0].prolation
    depthwise_offset_inventory = metrical_hierarchy.depthwise_offset_inventory

    #print 'OFFSETS'
    for depth, offsets in depthwise_offset_inventory.iteritems():
        offsets = [(x * prolation) + first_offset for x in offsets]
        #print '\t', depth, offsets
        depthwise_offset_inventory[depth] = tuple(offsets)


    def get_offsets_at_depth(depth):
        if depth in depthwise_offset_inventory:
            return depthwise_offset_inventory[depth]
        new_offsets = []
        old_offsets = depthwise_offset_inventory[depth - 1]
        for first, second in sequencetools.iterate_sequence_pairwise_strict(old_offsets):
            new_offsets.append(first)
            new_offsets.append((first + second) / 2)
        new_offsets.append(old_offsets[-1])
        depthwise_offset_inventory[depth] = new_offsets
        return tuple(new_offsets)

    def is_acceptable_tie_chain(tie_chain, offsets):
        if tie_chain.preprolated_duration.is_assignable:
            if tie_chain.start_offset in offsets:
                return True
            if tie_chain.stop_offset in offsets:
                return True
        return False

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        if is_acceptable_tie_chain(tie_chain, offsets):
            #print 'ACCEPTABLE:', tie_chain, tie_chain.start_offset, tie_chain.stop_offset
            #print '\t', offsets
            leaftools.fuse_leaves(tie_chain[:])
        else:
            #print 'UNACCEPTABLE:', tie_chain, tie_chain.start_offset, tie_chain.stop_offset
            #print '\t', offsets
            split_offset = None
            offsets = get_offsets_at_depth(depth + 1)
            for offset in offsets:
                if tie_chain.start_offset < offset < tie_chain.stop_offset:
                    split_offset = offset - tie_chain.start_offset
                    break
            #print '\t', split_offset
            if split_offset is not None:
                tie_chains = [tietools.TieChain(shard) for shard in
                    componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
                for tie_chain in tie_chains:
                    recurse(tie_chain, depth=depth+1)
            else:
                recurse(tie_chain, depth=depth+1)

    # cache results of iterator, as we'll be mutating the underlying collection
    items = tuple(tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(components))
    for item in items:
        #print 'ITEMS:', items
        if isinstance(item, tietools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            duration = sum([x.preprolated_duration for x in item])
            sub_metrical_hierarchy = timesignaturetools.MetricalHierarchy(duration)
            establish_metrical_hierarchy(item[:], sub_metrical_hierarchy)
