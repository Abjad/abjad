from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from collections import Iterable


def all_are_intervals_or_trees_or_empty(input):
    '''Recursively test if all elements of `input` are
    BoundedIntervals or IntervalTrees.
    An empty result also return as True.
    '''

    def recurse(x):
        if isinstance(x, Iterable) and \
        not isinstance(x, (basestring, IntervalTree, BoundedInterval)):
            return [a for i in x for a in recurse(i)]
        else:
            return [x]

    return all([isinstance(x, (BoundedInterval, IntervalTree)) \
        for x in recurse(input)])
