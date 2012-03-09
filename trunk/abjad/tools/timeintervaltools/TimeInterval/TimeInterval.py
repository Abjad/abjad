from collections import MutableMapping
import copy
from abjad import Fraction
from abjad.mixins import _Immutable
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools._TimeIntervalMixin._TimeIntervalMixin import _TimeIntervalMixin


class TimeInterval(_TimeIntervalMixin, MutableMapping):
    '''A start / stop pair, carrying some metadata.'''

    __slots__ = ('_data', '_start', '_stop')

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], TimeInterval):
            start, stop, data = args[0].start, args[0].stop, args[0]
        elif len(args) == 2:
            start, stop, data = args[0], args[1], {}
        elif len(args) == 3:
            start, stop, data = args[0], args[1], args[2]

        start, stop = Offset(start), Offset(stop)
        assert start < stop
        if isinstance(data, type(self)):
            data = data._data
        assert isinstance(data, dict)

        object.__setattr__(self, '_start', start)
        object.__setattr__(self, '_stop', stop)
        object.__setattr__(self, '_data', copy.copy(data))

    ### OVERLOADS ###

    def __delitem__(self, item):
        self._data.__delitem__(item)

    def __eq__(self, other):
        if type(other) == type(self) and \
            other.start == self.start and \
            other.stop == self.stop and \
            other._data == self._data:
                return True
        return False

    def __getitem__(self, item):
        return self._data.__getitem__(item)

    def __hash__(self):
        return id(self)

    def __iter__(self):
        for x in self._data:
            yield x

    def __len__(self):
        return len(self._data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self._class_name, self.start, self.stop, self._data)

    def __setitem__(self, item, value):
        self._data.__setitem__(item, value)

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
        assert isinstance(interval, type(self))
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
        assert isinstance(interval, type(self))
        if interval.start <= self.start and self.stop <= interval.stop:
            return True
        else:
            return False

    def is_container_of_interval(self, interval):
        '''True if interval contains `interval`.'''
        assert isinstance(interval, type(self))
        if self.start <= interval.start and interval.stop <= self.stop:
            return True
        else:
            return False

    def is_overlapped_by_interval(self, interval):
        '''True if interval is overlapped by `interval`.'''
        assert isinstance(interval, type(self))
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
        assert isinstance(interval, type(self))
        if self.stop == interval.start or interval.stop == self.start:
            return True
        else:
            return False

    def scale_by_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 <= rational
        if rational != 1:
            new_duration = (self.stop - self.start) * rational
            return type(self)(TimeInterval(self.start, self.start + new_duration, self))
        else:
            return self

    def scale_to_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 <= rational
        if rational != self.duration:
            return type(self)(TimeInterval(self.start, self.start + rational, self))
        else:
            return self

    def shift_by_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        if rational != 0:
            return type(self)(TimeInterval(self.start + rational, self.stop + rational, self))
        else:
            return self

    def shift_to_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        if rational != self.start:
            duration = self.stop - self.start
            return type(self)(TimeInterval(rational, rational + duration, self))
        else:
            return self

    def split_at_rationals(self, *rationals):
        assert 0 < len(rationals)
        assert all([isinstance(rational, (int, Fraction)) for rational in rationals])

        intervals = [self]
        new_intervals = [ ]
        for rational in sorted(rationals):
            for interval in intervals:
                if interval.start < rational < interval.stop:
                    new_intervals.append(type(self)(interval.start, rational, self))
                    new_intervals.append(type(self)(rational, interval.stop, self))
                else:
                    new_intervals.append(interval)
            intervals = new_intervals
            new_intervals = [ ]

        return tuple(sorted(intervals, key=lambda x: x.signature))
