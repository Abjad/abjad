from abc import ABCMeta
from abc import abstractmethod
from abjad import Duration
from abjad.tools.abctools import ImmutableAbjadObject


class _TimeIntervalMixin(ImmutableAbjadObject):

    __metaclass__ = ABCMeta

    __slots__ = ('_start', '_stop')

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
        assert isinstance(interval, _TimeIntervalMixin)
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
        assert isinstance(interval, _TimeIntervalMixin)
        if interval.start <= self.start and self.stop <= interval.stop:
            return True
        else:
            return False

    def is_container_of_interval(self, interval):
        '''True if interval contains `interval`.'''
        assert isinstance(interval, _TimeIntervalMixin)
        if self.start <= interval.start and interval.stop <= self.stop:
            return True
        else:
            return False

    def is_overlapped_by_interval(self, interval):
        '''True if interval is overlapped by `interval`.'''
        assert isinstance(interval, _TimeIntervalMixin)
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
        assert isinstance(interval, _TimeIntervalMixin)
        if self.stop == interval.start or interval.stop == self.start:
            return True
        else:
            return False

    @abstractmethod
    def scale_by_rational(self, rational):
        raise NotImplementedError

    @abstractmethod
    def scale_to_rational(self, rational):
        raise NotImplementedError

    @abstractmethod
    def shift_by_rational(self, rational):
        raise NotImplementedError

    @abstractmethod
    def shift_to_rational(self, rational):
        raise NotImplementedError

    @abstractmethod
    def split_at_rationals(self, *rationals):
        raise NotImplementedError
