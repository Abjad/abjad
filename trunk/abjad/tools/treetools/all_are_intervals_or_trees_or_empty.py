from collections import Iterable
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree


def all_are_intervals_or_trees_or_empty(input):
    '''Recursively test if all elements of `input` are
       `BoundedInterval`s or `IntervalTree`s.'''

    def recurse(x):
        if isinstance(x, Iterable) and \
        not isinstance(x, (basestring, IntervalTree)):
            return [a for i in x for a in recurse(i)]
        else:
            return [x]

    return all([isinstance(x, (BoundedInterval, IntervalTree)) \
        for x in recurse(input)])
