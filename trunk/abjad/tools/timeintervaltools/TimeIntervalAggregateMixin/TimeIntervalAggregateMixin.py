import abc
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeIntervalAggregateMixin(TimeIntervalMixin):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def earliest_start(self):
        raise NotImplementedError

    @abc.abstractproperty
    def earliest_stop(self):
        raise NotImplementedError

    @abc.abstractproperty
    def intervals(self):
        raise NotImplementedError

    @abc.abstractproperty
    def latest_start(self):
        raise NotImplementedError

    @abc.abstractproperty
    def latest_stop(self):
        raise NotImplementedError

    @property
    def offset_counts(self):
        from collections import Counter
        offsets = []
        for interval in self.intervals:
            offsets.append(interval.start)
            offsets.append(interval.stop)
        return dict(Counter(offsets))

    @property
    def offsets(self):
        offsets = []
        for interval in self.intervals:
            offsets.append(interval.start)
            offsets.append(interval.stop)
        return set(offsets)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def find_intervals_intersecting_or_tangent_to_interval(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_intersecting_or_tangent_to_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_after_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_and_stopping_within_interval(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_at_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_before_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_or_stopping_at_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_starting_within_interval(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_stopping_after_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_stopping_at_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_stopping_before_offset(self):
        raise NotImplementedError

    @abc.abstractmethod
    def find_intervals_stopping_within_interval(self):
        raise NotImplementedError
