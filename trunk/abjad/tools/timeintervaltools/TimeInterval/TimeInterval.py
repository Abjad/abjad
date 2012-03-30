from collections import MutableMapping
import copy
from abjad import Fraction
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeInterval(TimeIntervalMixin, MutableMapping):
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

    ### SPECIAL METHODS ###

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

    ### PUBLIC PROPERTIES ###

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

    def quantize_to_rational(self, rational):
        rational = Duration(rational)
        assert 0 < rational
        start = Offset(int(round(interval.start / rational))) * rational
        stop = Offset(int(round(interval.stop / rational))) * rational
        if start == stop:
            stop = start + rational
        return type(self)(start, stop, self)

    def scale_by_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 < rational
        if rational != 1:
            new_duration = (self.stop - self.start) * rational
            return type(self)(TimeInterval(self.start, self.start + new_duration, self))
        else:
            return self

    def scale_to_rational(self, rational):
        assert isinstance(rational, (int, Fraction))
        assert 0 < rational
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
                    new_intervals.append(type(self)(interval))
            intervals = new_intervals
            new_intervals = [ ]

        return tuple(sorted(intervals, key=lambda x: x.signature))
