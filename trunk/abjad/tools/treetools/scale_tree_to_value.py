from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree


def scale_tree_to_value(tree, value):

    assert isinstance(tree, IntervalTree)
    assert isinstance(value, (int, Fraction))
    assert 0 <= value

    if value == 1:
        return tree

    ratio = Fraction(value) / Fraction(tree.magnitude)
    tree_low = tree.low_min
    output_tree = IntervalTree([ ])
    for interval in tree:
        low = ((interval.low - tree_low) * ratio) + tree_low
        high = ((interval.high - tree_low) * ratio) + tree_low
        output_tree.insert(BoundedInterval(low, high, interval.data))

    return output_tree
