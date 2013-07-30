import abc
from abjad.tools import durationtools
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeIntervalAggregateMixin(TimeIntervalMixin):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @property
    def all_unique_bounds(self):
        values = []
        for interval in self.intervals:
            if interval.start_offset not in values:
                values.append(interval.start_offset)
            if interval.stop_offset not in values:
                values.append(interval.stop_offset)
        return tuple(sorted(values))
    
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

    def calculate_attack_density(self, bounding_interval=None):
        if bounding_interval is None:
            return len(self.intervals) / self.duration
        return len(self.find_intervals_starting_within_interval(
            bounding_interval)) / bounding_interval.duration

    def calculate_depth_centroid(self, bounding_interval=None):
        '''Calculate the weighted mean offset of `intervals`, such that the
        centroids of each interval in the depth tree of `intervals` make up
        the values of the mean, and the depth of each interval in the depth
        tree of `intervals` make up the weights.

        Return Offset.
        '''
        if not self:
            return None
        depth_tree = self.compute_depth(bounding_interval=bounding_interval)
        weighted_centroids = sum(interval.center * interval['depth']
            for interval in depth_tree)
        sum_of_weights = sum(interval['depth'] for interval in depth_tree)
        if not sum_of_weights:
            return None
        return durationtools.Offset(weighted_centroids) / sum_of_weights

    def calculate_depth_density(self, bounding_interval=None):
        '''Return a fraction, of the duration of each interval in the
        depth tree of `intervals`, multiplied by the depth at that interval,
        divided by the overall duration of `intervals`.

        The depth density of a single interval is `1`:

        Return multiplier.
        '''
        from abjad.tools import timeintervaltools
        tree = self
        if bounding_interval is not None:
            tree = timeintervaltools.TimeIntervalTree(
                tree.split_at_rationals(
                    bounding_interval.start_offset,
                    bounding_interval.stop_offset,
                    ))
            tree = \
                tree.find_intervals_starting_and_stopping_within_interval(
                bounding_interval)
        if not tree:
            return durationtools.Multiplier(0)
        duration_sum = sum(interval.duration for interval in tree)
        if bounding_interval is None:
            return duration_sum / tree.duration
        return duration_sum / bounding_interval.duration

    def calculate_mean_attack_offset(self):
        if not self:
            return None
        return durationtools.Offset(sum(interval.start_offset 
            for interval in self)) / len(self.intervals)

    def calculate_mean_release_offset(self):
        if not self:
            return None
        return durationtools.Offset(sum(interval.stop_offset 
            for interval in self)) / len(self.intervals)

    def calculate_minimum_mean_and_maximum_depths(self):
        '''Return a 3-tuple of the minimum, mean and maximum depth of 
        `intervals`.

        If `intervals` is empty, return None.
        
        "Mean" in this case is a weighted mean, where the durations of the 
        intervals in depth tree of `intervals` are the weights.
        '''
        if not self:
            return None
        depth_tree = self.compute_depth()
        depths = [interval['depth'] for interval in depth_tree]
        mean = self.calculate_depth_density()
        return min(depths), mean, max(depths)

    def calculate_minimum_mean_and_maximum_durations(self):
        '''Return a 3-tuple of the minimum, mean and maximum duration of all 
        intervals in `intervals`.

        If `intervals` is empty, return None.
        '''
        if not self.intervals:
            return None
        durations = [interval.duration for interval in self.intervals]
        minimum = min(durations)
        maximum = max(durations)
        mean = durationtools.Duration(sum(durations), len(durations))
        return minimum, mean, maximum

    def calculate_release_density(self, bounding_interval=None):
        if bounding_interval is None:
            return len(self.intervals) / self.duration
        return len(self.find_intervals_stopping_within_interval(
            bounding_interval)) / bounding_interval.duration

    def calculate_sustain_centroid(self):
        '''Return a weighted mean, such that the centroid of each interval
        in `intervals` are the values, and the weights are their durations.
        '''
        if not self:
            return None
        weighted_centroids = sum(interval.center * interval.duration 
            for interval in self.intervals)
        sum_of_weights = sum(interval.duration for interval in self.intervals)
        return durationtools.Offset(weighted_centroids) / sum_of_weights
        
    @abc.abstractmethod
    def clip_interval_durations_to_range(self, minimum=None, maximum=None):
        raise NotImplementedError

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
            all_bounds = list(bounded_tree.all_unique_bounds)
            while all_bounds[0] < bounding_interval.start_offset:
                all_bounds.pop(0)
            while bounding_interval.stop_offset < all_bounds[-1]:
                all_bounds.pop()
            if bounding_interval.start_offset < all_bounds[0]:
                all_bounds.insert(0, bounding_interval.start_offset)
            if all_bounds[-1] < bounding_interval.stop_offset:
                all_bounds.append(bounding_interval.stop_offset)
        else:
            all_bounds = list(self.all_unique_bounds)
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
    def fuse_overlapping_intervals(self, include_tangent_intervals=False):
        raise NotImplementedError

    def partition(self, include_tangent_intervals=False):
        '''Partition aggregate into groups of overlapping intervals:

        ::

            >>> tree = timeintervaltools.TimeIntervalTree(
            ...     timeintervaltools.make_test_intervals)
            >>> tree

        ::

            >>> for group in tree.partition():
            ...     group
            ...
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
                TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
                TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
                TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
                TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
            ])

        If `include_tangent_intervals` is true, treat tangent intervals as
        part of the same group:

        ::

            >>> for group in tree.partition(include_tangent_intervals=True):
            ...     group
            ...
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
                TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
                TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
                TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
                TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
                TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'})
            ])
            TimeIntervalTree([
                TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'}),
                TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
            ])
            
        Return 0 or more trees.
        '''
        from abjad.tools import timeintervaltools
        groups = []
        current_group = []
        intervals = self.intervals
        for current_interval in intervals:
            if not current_group:
                current_group.append(current_interval)
                continue
            if current_interval.start_offset < current_group[-1].stop_offset:
                current_group.append(current_interval)
            elif include_tangent_intervals and \
                current_interval.start_offset == current_group[-1].stop_offset:
                current_group.append(current_interval)
            else:
                groups.append(timeintervaltools.TimeIntervalTree(
                    current_group))
                current_group = [current_interval]
        if current_group:
            groups.append(timeintervaltools.TimeIntervalTree(current_group))
        return tuple(groups)

    @abc.abstractmethod
    def scale_interval_durations_by_rational(self, rational):
        raise NotImplementedError

    @abc.abstractmethod
    def scale_interval_durations_to_rational(self, rational):
        raise NotImplementedError

    @abc.abstractmethod
    def scale_interval_offsets_by_rational(self, rational):
        raise NotImplementedError
