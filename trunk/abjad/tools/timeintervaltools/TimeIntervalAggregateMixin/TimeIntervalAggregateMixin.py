from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from abjad import Duration
from abjad.exceptions import NotImplementedError
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeIntervalAggregateMixin(TimeIntervalMixin):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### PUBLIC ATTRIBUTES ###

    @abstractproperty
    def earliest_start(self):
        raise NotImplementedError

    @abstractproperty
    def earliest_stop(self):
        raise NotImplementedError

    @abstractproperty
    def intervals(self):
        raise NotImplementedError

    @abstractproperty
    def latest_start(self):
        raise NotImplementedError

    @abstractproperty
    def latest_stop(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @abstractmethod
    def find_intervals_intersecting_or_tangent_to_interval(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_intersecting_or_tangent_to_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_after_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_and_stopping_within_interval(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_at_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_before_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_or_stopping_at_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_starting_within_interval(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_stopping_after_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_stopping_at_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_stopping_before_offset(self):
        raise NotImplementedError

    @abstractmethod
    def find_intervals_stopping_within_interval(self):
        raise NotImplementedError
