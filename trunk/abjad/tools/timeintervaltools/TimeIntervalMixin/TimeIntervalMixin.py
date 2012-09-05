import abc
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class TimeIntervalMixin(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    def __nonzero__(self):
        return bool(self.duration)

    ### PUBLIC PROPERTIES ###

    @property
    def bounds(self):
        '''Start and stop of self returned as TimeInterval instance:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
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
        return timeintervaltools.TimeInterval(self.start, self.stop)

    @property
    def center(self):
        '''Center offset of start and stop offsets:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> interval = TimeInterval(2, 10)
            >>> interval.center
            Offset(6, 1)

        Returns `Offset` instance.
        '''
        if self.start is not None and self.stop is not None:
            return durationtools.Offset(self.stop + self.start) / 2
        raise UnboundedTimeIntervalError

    @property
    def duration(self):
        '''Duration of the time interval:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> interval = TimeInterval(2, 10)
            >>> interval.duration
            Duration(8, 1)

        Returns `Duration` instance.
        '''
        if self.start is not None and self.stop is not None:
            return durationtools.Duration(self.stop - self.start)
        raise UnboundedTimeIntervalError

    @property
    def signature(self):
        '''Tuple of start bound and stop bound.

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> interval = TimeInterval(2, 10)
            >>> interval.signature
            (Offset(2, 1), Offset(10, 1))

        Returns 2-tuple of `Offset` instances.
        '''
        if self.start is not None and self.stop is not None:
            return (self.start, self.stop)
        raise UnboundedTimeIntervalError

    @property
    def start(self):
        '''Starting offset of interval:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> interval = TimeInterval(2, 10)
            >>> interval.start
            Offset(2, 1)

        Returns `Offset` instance.
        '''
        return self._start

    @property
    def stop(self):
        '''Stopping offset of interval:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> interval = TimeInterval(2, 10)
            >>> interval.stop
            Offset(10, 1)

        Returns `Offset` instance.
        '''
        return self._stop

    ### PUBLIC METHODS ###

    def get_overlap_with_interval(self, interval):
        '''Return amount of overlap with `interval`.'''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError

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
        assert isinstance(interval, TimeIntervalMixin)

        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError

        if interval.start <= self.start and self.stop <= interval.stop:
            return True
        else:
            return False

    def is_container_of_interval(self, interval):
        '''True if interval contains `interval`.'''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError

        if self.start <= interval.start and interval.stop <= self.stop:
            return True
        else:
            return False

    def is_overlapped_by_interval(self, interval):
        '''True if interval is overlapped by `interval`.'''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError

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
        return False

    def is_tangent_to_interval(self, interval):
        '''True if interval is tangent to `interval`.'''
        assert isinstance(interval, TimeIntervalMixin)

        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError

        if self.stop == interval.start or interval.stop == self.start:
            return True
        else:
            return False

    @abc.abstractmethod
    def quantize_to_rational(self, rational):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedErro

    @abc.abstractmethod
    def scale_by_rational(self, rational):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def scale_to_rational(self, rational):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def shift_by_rational(self, rational):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def shift_to_rational(self, rational):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError

    @abc.abstractmethod
    def split_at_rationals(self, *rationals):
        if self.start is None or self.stop is None:
            raise UnboundedTimeIntervalError
        raise NotImplementedError
