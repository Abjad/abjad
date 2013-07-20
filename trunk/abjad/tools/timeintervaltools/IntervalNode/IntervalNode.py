import fractions
from abjad.tools.timeintervaltools.RedBlackNode import RedBlackNode


class IntervalNode(RedBlackNode):
    '''A red-black node in an TimeIntervalTree.
    Duplicate payloads are supported by maintaining a list of TimeIntervals
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        'earliest_stop',
        'key',
        'latest_stop',
        'left',
        'parent',
        'payload',
        'red', 
        'right',
        )

    ### INITIALIZER ###

    def __init__(self, key, intervals=None):
        from abjad.tools import timeintervaltools
        assert isinstance(key, (int, fractions.Fraction))
        RedBlackNode.__init__(self, key)
        self.payload = []
        if isinstance(intervals, (list, set, tuple)):
            assert all(isinstance(interval, timeintervaltools.TimeInterval) 
                for interval in intervals)
            self.payload.extend(intervals)
        elif isinstance(intervals, (timeintervaltools.TimeInterval, 
            type(None))):
            self.payload.append(intervals)
        else:
            raise ValueError('Only accepts single or multiple instances of TimeInterval.')

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s, %r)' % (self._class_name, self.key, self.payload)
