import abc
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeIntervalAggregateMixin(TimeIntervalMixin):

    ### CLASS VARIABLES ###

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
            offsets.append(interval.start_offset)
            offsets.append(interval.stop_offset)
        return dict(Counter(offsets))

    @property
    def offsets(self):
        offsets = []
        for interval in self.intervals:
            offsets.append(interval.start_offset)
            offsets.append(interval.stop_offset)
        return set(offsets)

    ### PUBLIC METHODS ###

    def compute_depth(self, bounding_interval=None):
        '''Compute a tree whose intervals represent the level of overlap
        of the time interval aggregate:

        ::

            >>> a = timeintervaltools.TimeInterval(0, 3)
            >>> b = timeintervaltools.TimeInterval(6, 12)
            >>> c = timeintervaltools.TimeInterval(9, 15)
            >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
            >>> tree.compute_depth()
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
                TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
                TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
                TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
                TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1})
            ])

        If `bounding_interval` is not none, only consider the depth of 
        time intervals which intersect that time interval:

        ::

            >>> a = timeintervaltools.TimeInterval(0, 3)
            >>> b = timeintervaltools.TimeInterval(6, 12)
            >>> c = timeintervaltools.TimeInterval(9, 15)
            >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
            >>> d = timeintervaltools.TimeInterval(-1, 16)
            >>> tree.compute_depth(bounding_interval=d)
            TimeIntervalTree([
                TimeInterval(Offset(-1, 1), Offset(0, 1), {'depth': 0}),
                TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
                TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
                TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
                TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
                TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1}),
                TimeInterval(Offset(15, 1), Offset(16, 1), {'depth': 0})
            ])
            
        Return interval tree.
        '''
        from abjad.tools import sequencetools
        from abjad.tools import timeintervaltools
        if bounding_interval is not None:
            bounded_tree = self.find_intervals_intersecting_or_tangent_to_interval(
                bounding_interval)
            if not bounded_tree:
                return timeintervaltools.TimeIntervalTree([
                    timeintervaltools.TimeInterval(
                        bounding_interval.start_offset, 
                        bounding_interval.stop_offset, 
                        {'depth': 0},
                        )
                    ])
            all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(
                bounded_tree))
            while all_bounds[0] < bounding_interval.start_offset:
                all_bounds.pop(0)
            while bounding_interval.stop_offset < all_bounds[-1]:
                all_bounds.pop()
            if bounding_interval.start_offset < all_bounds[0]:
                all_bounds.insert(0, bounding_interval.start_offset)
            if all_bounds[-1] < bounding_interval.stop_offset:
                all_bounds.append(bounding_interval.stop_offset)
        else:
            all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(
                self))
        depth_intervals = []
        for start_offset, stop_offset in sequencetools.iterate_sequence_pairwise_strict(
            all_bounds):
            current_interval = timeintervaltools.TimeInterval(
                start_offset, stop_offset, {})
            found = self.find_intervals_intersecting_or_tangent_to_interval(
                current_interval)
            depth = 0
            if found:
                depth = len([x for x in found 
                    if (not x.start_offset == current_interval.stop_offset 
                    and not x.stop_offset == current_interval.start_offset)])
            current_interval['depth'] = depth
            depth_intervals.append(current_interval)
        return timeintervaltools.TimeIntervalTree(depth_intervals)

    def compute_logical_and(self, bounding_interval=None):
        '''Compute logical AND of intervals.

        Return time interval tree.
        '''
        from abjad.tools import timeintervaltools
        return timeintervaltools.TimeIntervalTree((
            x for x in self.compute_depth(bounding_interval=bounding_interval)
            if 1 < x['depth']))

    def compute_logical_not(self, bounding_interval=None):
        '''Compute logical NOT of intervals.

        Return time interval tree.
        '''
        from abjad.tools import timeintervaltools
        return timeintervaltools.TimeIntervalTree((
            x for x in self.compute_depth(bounding_interval=bounding_interval)
            if x['depth'] == 0))

    def compute_logical_or(self, bounding_interval=None):
        '''Compute logical OR of intervals.

        Return time interval tree.
        '''
        from abjad.tools import timeintervaltools
        return timeintervaltools.TimeIntervalTree((
            x for x in self.compute_depth(bounding_interval=bounding_interval)
            if 1 <= x['depth']))

    def compute_logical_xor(self, bounding_interval=None):
        '''Compute logical XOR of intervals.

        Return time interval tree.
        '''
        from abjad.tools import timeintervaltools
        return timeintervaltools.TimeIntervalTree((
            x for x in self.compute_depth(bounding_interval=bounding_interval)
            if x['depth'] == 1))

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

    @abc.abstractmethod
    def scale_interval_durations_by_rational(self, rational):
        raise NotImplementedError

    @abc.abstractmethod
    def scale_interval_durations_to_rational(self, rational):
        raise NotImplementedError

    @abc.abstractmethod
    def scale_interval_offsets_by_rational(self, rational):
        raise NotImplementedError
