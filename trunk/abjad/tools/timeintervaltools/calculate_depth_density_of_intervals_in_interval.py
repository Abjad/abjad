import fractions


def calculate_depth_density_of_intervals_in_interval(intervals, interval):
    '''Return a Fraction, of the duration of each interval in the
    depth tree of `intervals` within `interval`, multiplied by the depth at that interval,
    divided by the overall duration of `intervals`.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    split_tree = timeintervaltools.split_intervals_at_rationals(tree, [interval.start, interval.stop])
    split_tree = timeintervaltools.TimeIntervalTree(
        split_tree.find_intervals_starting_and_stopping_within_interval(interval))

    if not split_tree:
        return fractions.Fraction(0)

    return fractions.Fraction(sum([x.duration for x in split_tree])) / interval.duration
