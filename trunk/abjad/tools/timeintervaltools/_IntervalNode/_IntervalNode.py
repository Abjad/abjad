from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools._RedBlackNode import _RedBlackNode
from fractions import Fraction


class _IntervalNode(_RedBlackNode):
    '''A red-black node in an TimeIntervalTree.
    Duplicate payloads are supported by maintaining a list of TimeIntervals
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('latest_stop', 'earliest_stop', 'key',
                'left', 'parent', 'payload', 'red', 'right', )

    ### INITIALIZER ###

    def __init__(self, key, intervals=None):
        assert isinstance(key, (int, Fraction))
        _RedBlackNode.__init__(self, key)
        self.payload = []
        if isinstance(intervals, (list, set, tuple)):
            assert all([isinstance(interval, TimeInterval) for interval in intervals])
            self.payload.extend(intervals)
        elif isinstance(intervals, (TimeInterval, type(None))):
            self.payload.append(intervals)
        else:
            raise ValueError('_IntervalNode only accepts single or multiple instances of TimeInterval.')

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s, %r)' % (type(self).__name__, self.key, self.payload)
