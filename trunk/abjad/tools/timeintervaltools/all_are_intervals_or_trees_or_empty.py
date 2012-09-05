import collections


def all_are_intervals_or_trees_or_empty(input):
    '''Recursively test if all elements of `input` are
    TimeIntervals or TimeIntervalTrees.
    An empty result also return as True.
    '''
    from abjad.tools import timeintervaltools

    def recurse(x):
        if isinstance(x, collections.Iterable) and \
        not isinstance(x, (basestring,
            timeintervaltools.TimeIntervalTree,
            timeintervaltools.TimeInterval)):
            return [a for i in x for a in recurse(i)]
        else:
            return [x]

    return all([isinstance(x, (timeintervaltools.TimeInterval,
        timeintervaltools.TimeIntervalTree))
        for x in recurse(input)])
