def calculate_density_of_attacks_in_interval(intervals, interval):
    '''Calculate the number of attacks in `interval` over the duration of `interval`.

    Return Fraction.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    return len(tree.find_intervals_starting_within_interval(interval)) \
        / interval.duration
