from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.compute_logical_not_of_intervals import compute_logical_not_of_intervals
from abjad.tools.treetools.split_intervals_in_tree_at_values import split_intervals_in_tree_at_values
from abjad.tools.treetools.get_all_unique_bounds_in_tree import get_all_unique_bounds_in_tree


def mask_intervals_with_intervals_while_preserving_payloads(masked_intervals, mask_intervals):
    '''Clip or remove all intervals in `masked_intervals` outside of the bounds
    defined in `mask_intervals`, while maintaining `masked_intervals`' payload contents ::

        abjad> tree = IntervalTree([ ])
        abjad> tree.insert(BoundedInterval(0, 10, 'a'))
        abjad> tree.insert(BoundedInterval(5, 15, 'b'))
        abjad> mask = BoundedInterval(4, 11)
        abjad> mask_intervals_with_intervals_while_preserving_payloads(tree, mask)
        IntervalTree([
            BoundedInterval(4, 10, data = 'a'),
            BoundedInterval(5, 11, data = 'b')
        ])
    '''    

    masked_tree = IntervalTree(masked_intervals)
    mask_tree = IntervalTree(mask_intervals)
    not_mask_tree = compute_logical_not_of_intervals(mask_tree)

    if masked_tree.low < mask_tree.low:
        not_mask_tree.insert(BoundedInterval(masked_tree.low, mask_tree.low))
    if mask_tree.high < masked_tree.high:
        not_mask_tree.insert(BoundedInterval(mask_tree.high, masked_tree.high))
    split_masked_tree = split_intervals_in_tree_at_values(masked_tree, \
        get_all_unique_bounds_in_tree(not_mask_tree))

    print 'not_mask:', repr(not_mask_tree)
    print 'split_masked:', repr(split_masked_tree)

    for interval in not_mask_tree:
        starts = split_masked_tree.find_intervals_starting_within_interval(interval)
        stops = split_masked_tree.find_intervals_stopping_within_interval(interval)
        split_masked_tree.remove(list(set(starts).intersection(set(stops))))

    return split_masked_tree
        
