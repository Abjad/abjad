import fractions


def calculate_depth_density_of_intervals(intervals):
    '''Return a Fraction, of the duration of each interval in the
    depth tree of `intervals`, multiplied by the depth at that interval,
    divided by the overall duration of `intervals`.

    The depth density of a single interval is 1 ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(0, 1)
        >>> b = TimeInterval(0, 1)
        >>> c = TimeInterval(Fraction(1, 2), 1)
        >>> timeintervaltools.calculate_depth_density_of_intervals(a)
        Duration(1, 1)
        >>> timeintervaltools.calculate_depth_density_of_intervals([a, b])
        Duration(2, 1)
        >>> timeintervaltools.calculate_depth_density_of_intervals([a, c])
        Duration(3, 2)
        >>> timeintervaltools.calculate_depth_density_of_intervals([a, b, c])
        Duration(5, 2)

    Return fraction.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return fractions.Fraction(0)

    return fractions.Fraction(sum([x.duration for x in tree])) / tree.duration
