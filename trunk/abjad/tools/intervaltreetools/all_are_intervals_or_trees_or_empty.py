from abjad.tools.intervaltreetools.TimeInterval import TimeInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from collections import Iterable


def all_are_intervals_or_trees_or_empty(input):
    '''Recursively test if all elements of `input` are
    TimeIntervals or IntervalTrees.
    An empty result also return as True.
    '''

    def recurse(x):
        if isinstance(x, Iterable) and \
        not isinstance(x, (basestring, IntervalTree, TimeInterval)):
            return [a for i in x for a in recurse(i)]
        else:
            return [x]

    return all([isinstance(x, (TimeInterval, IntervalTree)) \
        for x in recurse(input)])
