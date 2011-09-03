from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools._RedBlackNode import _RedBlackNode
from abjad import Fraction


class _IntervalNode(_RedBlackNode):
    '''A red-black node in an IntervalTree.
    Duplicate payloads are supported by maintaining a list of BoundedIntervals
    '''

    __slots__ = ('high_max', 'high_min', 'key',
                'left', 'parent', 'payload', 'red', 'right', )

    def __init__(self, key, intervals = None):
        assert isinstance(key, (int, Fraction))
        _RedBlackNode.__init__(self, key)
        self.payload = []
        if isinstance(intervals, (list, set, tuple)):
            assert all([isinstance(interval, BoundedInterval) for interval in intervals])
            self.payload.extend(intervals)
        elif isinstance(intervals, (BoundedInterval, type(None))):
            self.payload.append(intervals)
        else:
            raise ValueError('_IntervalNode only accepts single or multiple instances of BoundedInterval.')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s, %r)' % (type(self).__name__, self.key, self.payload)
