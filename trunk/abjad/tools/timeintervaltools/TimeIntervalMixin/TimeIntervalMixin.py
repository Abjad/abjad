# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class TimeIntervalMixin(AbjadObject):
    r'''Time-interval mixin.

    For examples:

    ::

        >>> from abjad.tools.timeintervaltools import TimeInterval

    Time-interval mixins provide time-interval functionality.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __nonzero__(self):
        return bool(self.duration)

    ### PUBLIC PROPERTIES ###

    @property
    def bounds(self):
        r'''Start and stop_offset of self returned as TimeInterval instance:

        ::

            >>> interval = TimeInterval(2, 10)
            >>> bounds = interval.bounds
            >>> bounds
            TimeInterval(Offset(2, 1), Offset(10, 1), {})
            >>> bounds == interval
            True
            >>> bounds is interval
            False

        Returns `TimeInterval` instance.
        '''
        from abjad.tools import timeintervaltools
        return timeintervaltools.TimeInterval(self.start_offset, self.stop_offset)

    @property
    def center(self):
        r'''Center offset of start_offset and stop_offset offsets:

        ::

            >>> interval = TimeInterval(2, 10)
            >>> interval.center
            Offset(6, 1)

        Returns `Offset` instance.
        '''
        if self.start_offset is not None and self.stop_offset is not None:
            return durationtools.Offset(self.stop_offset + self.start_offset) / 2
        raise UnboundedTimeIntervalError

    @property
    def duration(self):
        r'''Duration of the time interval:

        ::

            >>> interval = TimeInterval(2, 10)
            >>> interval.duration
            Duration(8, 1)

        Returns `Duration` instance.
        '''
        if self.start_offset is not None and self.stop_offset is not None:
            return durationtools.Duration(self.stop_offset - self.start_offset)
        raise UnboundedTimeIntervalError

    @property
    def signature(self):
        r'''Tuple of start_offset bound and stop_offset bound.

        ::

            >>> interval = TimeInterval(2, 10)
            >>> interval.signature
            (Offset(2, 1), Offset(10, 1))

        Returns 2-tuple of `Offset` instances.
        '''
        if self.start_offset is not None and self.stop_offset is not None:
            return (self.start_offset, self.stop_offset)
        raise UnboundedTimeIntervalError

    @property
    def start_offset(self):
        r'''Starting offset of interval:

        ::

            >>> interval = TimeInterval(2, 10)
            >>> interval.start_offset
            Offset(2, 1)

        Returns `Offset` instance.
        '''
        return self._start

    @property
    def stop_offset(self):
        r'''Stopping offset of interval:

        ::

            >>> interval = TimeInterval(2, 10)
            >>> interval.stop_offset
            Offset(10, 1)

        Returns `Offset` instance.
        '''
        return self._stop

    ### PUBLIC METHODS ###

    def get_overlap_with_interval(self, interval):
        r'''Returns amount of overlap with `interval`.
        '''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError

        if not self.is_overlapped_by_interval(interval):
            return 0
        elif self.is_container_of_interval(interval):
            return interval.duration
        elif self.is_contained_by_interval(interval):
            return self.duration
        elif self.start_offset < interval.start_offset:
            return self.stop_offset - interval.start_offset
        else:
            return interval.stop_offset - self.start_offset

    def is_contained_by_interval(self, interval):
        r'''True if interval is contained by `interval`.
        '''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError

        if interval.start_offset <= self.start_offset and self.stop_offset <= interval.stop_offset:
            return True
        else:
            return False

    def is_container_of_interval(self, interval):
        r'''True if interval contains `interval`.
        '''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError

        if self.start_offset <= interval.start_offset and interval.stop_offset <= self.stop_offset:
            return True
        else:
            return False

    def is_overlapped_by_interval(self, interval):
        r'''True if interval is overlapped by `interval`.
        '''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError

        if self.is_container_of_interval(interval):
            return True
        elif self.is_contained_by_interval(interval):
            return True
        elif self.start_offset < interval.start_offset < self.stop_offset:
            return True
        elif self.start_offset == interval.start_offset:
            return True
        elif self.stop_offset == interval.stop_offset:
            return True
        elif self.start_offset < interval.stop_offset < self.stop_offset:
            return True
        return False

    def is_tangent_to_interval(self, interval):
        r'''True if interval is tangent to `interval`.
        '''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError

        if self.stop_offset == interval.start_offset or interval.stop_offset == self.start_offset:
            return True
        else:
            return False

    @abc.abstractmethod
    def quantize_to_rational(self, rational):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedErro

    @abc.abstractmethod
    def scale_by_rational(self, rational):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def scale_to_rational(self, rational):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def shift_by_rational(self, rational):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def shift_to_rational(self, rational):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def split_at_rationals(self, *rationals):
        if self.start_offset is None or self.stop_offset is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError
