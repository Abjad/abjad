from abjad import Fraction
from abjad.core import _Immutable
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset

class BoundedInterval(dict, _Immutable):
    '''A start / stop pair, carrying some metadata.'''

    __slots__ = ('_stop', '_start', )

    def __init__(self, *args):
        dict.__init__(self)

        if len(args) == 1 and isinstance(args[0], BoundedInterval):
            start, stop, data = args[0].start, args[0].stop, args[0]
        elif len(args) == 2:
            start, stop, data = args[0], args[1], {}
        elif len(args) == 3:
            start, stop, data = args[0], args[1], args[2]

        assert isinstance(start, (int, Fraction))
        assert isinstance(stop, (int, Fraction))
        assert start < stop
        assert isinstance(data, dict)

        object.__setattr__(self, '_start', Offset(start))
        object.__setattr__(self, '_stop', Offset(stop))

        self.update(data)

    ### OVERLOADS ###

    def __eq__(self, other):
        if type(other) == type(self):
            if other.start == self.start:
                if other.stop == self.stop:
                    if dict.__eq__(self, other):
                        return True
        return False

    def __hash__(self):
        return id(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s(%s, %s, %s)' % \
            (type(self).__name__, \
            repr(self.start), \
            repr(self.stop), \
            dict.__repr__(self))

    ### PUBLIC ATTRIBUTES ###

    @property
    def center(self):
        '''Center point of start and stop bounds.'''
        return Offset(self.stop + self.start) / 2

    @property
    def duration(self):
        '''stop bound minus start bound.'''
        return Duration(self.stop - self.start)

    @property
    def signature(self):
        '''Tuple of start bound and stop bound.'''
        return (self.start, self.stop)

    @property
    def start(self):
        '''start bound.'''
        return self._start

    @property
    def stop(self):
        '''stop bound.'''
        return self._stop

    ### PUBLIC METHODS ###

    def get_overlap_with_interval(self, interval):
        '''Return amount of overlap with `interval`.'''
        assert isinstance(interval, BoundedInterval)
        if not self.is_overlapped_by_interval(interval):
            return 0
        elif self.is_container_of_interval(interval):
            return interval.duration
        elif self.is_contained_by_interval(interval):
            return self.duration
        elif self.start < interval.start:
            return self.stop - interval.start
        else:
            return interval.stop - self.start

    def is_contained_by_interval(self, interval):
        '''True if interval is contained by `interval`.'''
        assert isinstance(interval, BoundedInterval)
        if interval.start <= self.start and self.stop <= interval.stop:
            return True
        else:
            return False

    def is_container_of_interval(self, interval):
        '''True if interval contains `interval`.'''
        assert isinstance(interval, BoundedInterval)
        if self.start <= interval.start and interval.stop <= self.stop:
            return True
        else:
            return False

    def is_overlapped_by_interval(self, interval):
        '''True if interval is overlapped by `interval`.'''
        assert isinstance(interval, BoundedInterval)
        if self.is_container_of_interval(interval):
            return True
        elif self.is_contained_by_interval(interval):
            return True
        elif self.start < interval.start < self.stop:
            return True
        elif self.start == interval.start:
            return True
        elif self.stop == interval.stop:
            return True
        elif self.start < interval.stop < self.stop:
            return True
        else:
            return False

    def is_tangent_to_interval(self, interval):
        '''True if interval is tangent to `interval`.'''
        assert isinstance(interval, BoundedInterval)
        if self.stop == interval.start or interval.stop == self.start:
            return True
        else:
            return False

    def scale_by_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 <= rational
        if rational != 1:
            new_duration = (self.stop - self.start) * rational
            return type(self)(BoundedInterval(self.start, self.start + new_duration, self))
        else:
            return self

    def scale_to_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 <= rational
        if rational != self.duration:
            return type(self)(BoundedInterval(self.start, self.start + rational, self))
        else:
            return self

    def shift_by_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        if rational != 0:
            return type(self)(BoundedInterval(self.start + rational, self.stop + rational, self))
        else:
            return self

    def shift_to_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        if rational != self.start:
            duration = self.stop - self.start
            return type(self)(BoundedInterval(rational, rational + duration, self))
        else:
            return self

    def split_at_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        if self.start < rational < self.stop:
            return (type(self)(BoundedInterval(self.start, rational, self)),
                    type(self)(BoundedInterval(rational, self.stop, self)))
        else:
            return (self,)
