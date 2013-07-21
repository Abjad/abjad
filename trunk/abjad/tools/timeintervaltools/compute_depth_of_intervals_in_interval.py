from abjad.tools import sequencetools


def compute_depth_of_intervals_in_interval(intervals, bounding_interval):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`, cropped within `interval`::

        >>> from abjad.tools.timeintervaltools import *
        >>> a = TimeInterval(0, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 15)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> d = TimeInterval(-1, 16)
        >>> compute_depth_of_intervals_in_interval(tree, d)
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(0, 1), {'depth': 0}),
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1}),
            TimeInterval(Offset(15, 1), Offset(16, 1), {'depth': 0})
        ])

    Return interval tree.
    '''
    from abjad.tools import timeintervaltools

    return timeintervaltools.compute_depth_of_intervals(
        intervals,
        bounding_interval=bounding_interval,
        )
