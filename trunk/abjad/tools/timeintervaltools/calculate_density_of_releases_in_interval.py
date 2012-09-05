import fractions


def calculate_density_of_releases_in_interval(intervals, interval):
    '''Calculate the number of releases in `interval` divided by the duration of `interval`.

    Return Fraction.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    return fractions.Fraction(len(tree.find_intervals_stopping_within_interval(interval))) \
        / interval.duration
