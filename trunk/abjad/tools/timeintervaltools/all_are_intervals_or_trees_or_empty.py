from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from collections import Iterable


def all_are_intervals_or_trees_or_empty(input):
    '''Recursively test if all elements of `input` are
    TimeIntervals or TimeIntervalTrees.
    An empty result also return as True.
    '''

    def recurse(x):
        if isinstance(x, Iterable) and \
        not isinstance(x, (basestring, TimeIntervalTree, TimeInterval)):
            return [a for i in x for a in recurse(i)]
        else:
            return [x]

    return all([isinstance(x, (TimeInterval, TimeIntervalTree)) \
        for x in recurse(input)])
