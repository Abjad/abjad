from abjad.tools import durationtools


def calculate_mean_release_of_intervals(intervals):
    '''Return a Fraction of the average release offset of `intervals`.'''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    return durationtools.Offset(sum([i.stop for i in tree])) / len(tree)
