import copy
from collections import Iterable
from abjad import Fraction
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin import TimeIntervalAggregateMixin
from abjad.tools.timeintervaltools._IntervalNode import _IntervalNode
from abjad.tools.timeintervaltools._RedBlackTree import _RedBlackTree


class TimeIntervalTree(_RedBlackTree, TimeIntervalAggregateMixin):
    '''An augmented red-black tree for storing and searching for intervals of
    time (rather than pitch).

    This allows for the arbitrary placement of blocks of material along a
    time-line.  While this functionality could be achieved with Python's
    built-in collections, this class reduces the complexity of the search
    process, such as locating overlapping intervals.

    TimeIntervalTrees can be instantiated without contents, or from a mixed
    collection of other TimeIntervalTrees and / or TimeIntervals.  The input
    will be parsed recursively ::

        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> interval_one = TimeInterval(0, 10)
        abjad> interval_two = TimeInterval(1, 8)
        abjad> interval_three = TimeInterval(3, 13)
        abjad> tree = TimeIntervalTree([interval_one, interval_two, interval_three])

    '''

    __slots__ = ('_root', '_sentinel')

    def __init__(self, intervals = []):
        self._sentinel = _IntervalNode(0)
        self._sentinel.red = True
        self._sentinel.left = self._sentinel
        self._sentinel.right = self._sentinel
        self._sentinel.parent = self._sentinel
        self._root = self._sentinel
        self._insert(intervals)

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        if item in self._inorder:
            return True
        else:
            return False

    def __copy__(self):
        return TimeIntervalTree([copy.copy(x) for x in self])

    def __eq__(self, other):
        if type(self) == type(other):
            if self[:] == other[:]:
                return True
        return False

    def __getitem__(self, item):
        return self._inorder.__getitem__(item)

    def __getslice__(self, start, end):
        return self._inorder.__getslice__(start, end)

    def __iter__(self):
        for interval in self._inorder:
            yield interval

    def __len__(self):
        def recurse(node):
            length = 0
            if node != self._sentinel:
                length += len(node.payload)
            if node.left != self._sentinel:
                length += recurse(node.left)
            if node.right != self._sentinel:
                length += recurse(node.right)
            return length
        if self._root != self._sentinel:
            return recurse(self._root)
        else:
            return 0

    def __nonzero__(self):
        return bool(len(self))

    def __repr__(self):
        if self:
            intervals = [repr(interval) for interval in self._inorder]
            return '%s([\n\t%s\n])' % (type(self).__name__, ',\n\t'.join(intervals))
        else:
            return '%s([])' % type(self).__name__

    # PRIVATE ATTRIBUTES

    @property
    def _inorder(self):
        if self:
            intervals = []
            nodes = tuple(self._sort_nodes_inorder())
            for node in nodes:
                intervals.extend(sorted(node.payload, key=lambda x: x.signature))
            return tuple(intervals)
        else:
            return ()

    ### PRIVATE METHODS ###

    def _insert(self, args):
        def recurse(x):
            if isinstance(x, TimeInterval): # TimeIntervals are Iterable!
                return [x]
            elif isinstance(x, Iterable) and \
            not isinstance(x, (basestring)):
                return [a for i in x for a in recurse(i)]

        intervals = recurse(args)
        assert all([isinstance(x, TimeInterval) for x in intervals])

        for interval in intervals:
            node = self._find_by_key(interval.start)
            if node is not None:
                node.payload.append(interval)
            else:
                node = _IntervalNode(interval.start, interval)
                node.left = self._sentinel
                node.right = self._sentinel
                node.parent = self._sentinel
                self._insert_node(node)
        self._update_stop_extrema()

    ### PUBLIC PROPERTIES ###

    @property
    def bounds(self):
        '''The startest and stopest values of the tree returned as a
        ``TimeInterval`` instance:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.bounds
            TimeInterval(Offset(1, 1), Offset(7, 2), {})

        Returns ``TimeInterval`` instance, or None if tree is empty.
        '''
        if self:
            return TimeInterval(self.start, self.stop)
        return None

    @property
    def duration(self):
        '''Absolute difference of the stop and start values of the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.duration
            Duration(5, 2)

        Empty trees have a duration of 0.

        Returns ``Duration`` instance.
        '''
        if self:
            return Duration(self.latest_stop - self.earliest_start)
        else:
            return Duration(0)

    @property
    def earliest_start(self):
        '''The minimum start value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.earliest_start
            Offset(1, 1)

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return Offset(self._find_minimum(self._root).key)
        else:
            return None

    @property
    def earliest_stop(self):
        '''The minimum stop value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.earliest_stop
            Offset(2, 1)

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return Offset(self._root.earliest_stop)
        else:
            return None

    @property
    def latest_start(self):
        '''The maximum start value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.latest_start
            Offset(3, 1)

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return Offset(self._find_maximum(self._root).key)
        else:
            return None

    @property
    def latest_stop(self):
        '''The maximum stop value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.latest_stop
            Offset(7, 2)

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return Offset(self._root.latest_stop)
        else:
            return None

    @property
    def start(self):
        '''The minimum start value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.start
            Offset(1, 1)

        Alias of earliest_start.

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        return self.earliest_start

    @property
    def stop(self):
        '''The maximum stop value of all intervals in the tree:

        ::

            abjad> from abjad.tools.timeintervaltools import *
            abjad> ti1 = TimeInterval(1, 2)
            abjad> ti2 = TimeInterval(3, (7, 2))
            abjad> tree = TimeIntervalTree([ti1, ti2])
            abjad> tree.stop
            Offset(7, 2)

        Alias of latest_stop.

        Returns ``Offset`` instance, or None if tree is empty.
        '''
        return self.latest_stop

    ### PRIVATE METHODS ###

    def _update_stop_extrema(self):
        def recurse(node):
            max = min = node.payload[0].stop
            for interval in node.payload[1:]:
                if max < interval.stop:
                    max = interval.stop
                if interval.stop < min:
                    min = interval.stop
            if node.left != self._sentinel:
                left_max, left_min = recurse(node.left)
                if max < left_max:
                    max = left_max
                if left_min < min:
                    min = left_min
            if node.right != self._sentinel:
                right_max, right_min = recurse(node.right)
                if max < right_max:
                    max = right_max
                if right_min < min:
                    min = right_min
            node.latest_stop = max
            node.earliest_stop = min
            return max, min
        if self._root != self._sentinel:
            recurse(self._root)

    ### PUBLIC METHODS ###

    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        def recurse(node, start, stop):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key <= stop and start <= node.latest_stop:
                for interval in node.payload:
                    if interval.start <= stop and start <= interval.stop:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and self._find_minimum(node.left).key <= stop \
                and start <= node.left.latest_stop:
                intervals.extend(recurse(node.left, start, stop))
            if node.right != self._sentinel \
                and self._find_minimum(node.right).key <= stop \
                and start <= node.right.latest_stop:
                intervals.extend(recurse(node.right, start, stop))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], TimeInterval)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, start, stop), key=lambda x: x.signature))

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key <= offset and offset <= node.latest_stop:
                for interval in node.payload:
                    if interval.start <= offset and offset <= interval.stop:
                        intervals.append(interval)
            if node.left != self._sentinel and self._find_minimum(node.left).key <= offset \
                and offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and self._find_minimum(node.right).key <= offset \
                and offset <= node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_after_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if offset < node.key:
                intervals.extend(node.payload)
            if node.left != self._sentinel and offset < self._find_maximum(node.left).key:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        def recurse(node, start, stop):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start <= node.key and node.earliest_stop <= stop:
                for interval in node.payload:
                    if start <= interval.start and interval.stop <= stop:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and start <= self._find_maximum(node.left).key \
                and node.left.earliest_stop <= stop:
                intervals.extend(recurse(node.left, start, stop))
            if node.right != self._sentinel \
                and start <= self._find_maximum(node.right).key \
                and node.right.earliest_stop <= stop:
                intervals.extend(recurse(node.right, start, stop))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], TimeInterval)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, start, stop), key=lambda x: x.signature))

    def find_intervals_starting_at_offset(self, offset):
        assert isinstance(offset, (int, Fraction))
        node = self._find_by_key(offset)
        if node is not None and node != self._sentinel:
            return tuple(sorted(node.payload, key=lambda x: x.signature))
        else:
            return ()

    def find_intervals_starting_before_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key < offset:
                intervals.extend(node.payload)
            if node.left != self._sentinel:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and self._find_minimum(node.right).key < offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key <= offset and offset <= node.latest_stop:
                for interval in node.payload:
                    if interval.start == offset or interval.stop == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and self._find_minimum(node.right).key <= offset \
                and offset <= node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_within_interval(self, *args):
        def recurse(node, start, stop):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start <= node.key <= stop:
                intervals.extend(node.payload)
            if node.left != self._sentinel and \
                start <= self._find_maximum(node.left).key and \
                self._find_minimum(node.left).key <= stop:
                intervals.extend(recurse(node.left, start, stop))
            if node.right != self._sentinel and \
                start <= self._find_maximum(node.right).key and \
                self._find_minimum(node.right).key <= stop:
                intervals.extend(recurse(node.right, start, stop))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], TimeInterval)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, start, stop), key=lambda x: x.signature))

    def find_intervals_stopping_after_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if offset < node.latest_stop:
                for interval in node.payload:
                    if offset < interval.stop:
                        intervals.append(interval)
            if node.left != self._sentinel and offset < node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and offset < node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_at_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.earliest_stop <= offset and offset <= node.latest_stop:
                for interval in node.payload:
                    if interval.stop == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and node.right.earliest_stop <= offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_before_offset(self, offset):
        def recurse(node, offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key <= offset and node.earliest_stop < offset:
                for interval in node.payload:
                    if interval.stop < offset:
                        intervals.append(interval)
            if node.left != self._sentinel and node.left.earliest_stop < offset:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and node.right.earliest_stop < offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_within_interval(self, *args):
        def recurse(node, start, stop):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start <= node.latest_stop and node.earliest_stop <= stop:
                for interval in node.payload:
                    if start <= interval.stop <= stop:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                start <= node.left.latest_stop and \
                node.left.earliest_stop <= stop:
                intervals.extend(recurse(node.left, start, stop))
            if node.right != self._sentinel and \
                start <= node.right.latest_stop and \
                node.right.earliest_stop <= stop:
                intervals.extend(recurse(node.right, start, stop))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], TimeInterval)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, start, stop), key=lambda x: x.signature))

    def scale_by_rational(self, rational):
        rational = Duration(rational)
        return TimeIntervalTree([
            x.shift_to_rational(
                ((x.start - self.start) * rational) + self.start).scale_by_rational(rational)\
                for x in self
        ])

    def scale_to_rational(self, rational):
        rational = Duration(rational)
        ratio = rational / self.duration
        return TimeIntervalTree([
            x.shift_to_rational(
                ((x.start - self.start) * ratio) + self.start).scale_by_rational(ratio) \
                for x in self])

    def shift_by_rational(self, rational):
        rational = Offset(rational)
        return TimeIntervalTree([
            x.shift_by_rational(rational) for x in self
        ])

    def shift_to_rational(self, rational):
        rational = Offset(rational)
        return TimeIntervalTree([
            x.shift_by_rational(rational - self.start) for x in self
        ])

    def split_at_rationals(self, *rationals):
        assert 0 < len(rationals)
        rationals = tuple(sorted([Offset(x) for x in rationals]))

        trees = []
        intervals = self[:]
        before = []
        after = []
        for rational in rationals:
            for interval in intervals:
                splits = interval.split_at_rationals(rational)
                if len(splits) == 1:
                    if splits[0].stop <= rational:
                        before.append(splits[0])
                    elif rational <= splits[0].start:
                        after.append(splits[0])
                else:
                    before.append(splits[0])
                    after.append(splits[1])

            if before:
                trees.append(TimeIntervalTree(before))

            intervals = after
            before = []
            after = []

        if intervals:
            trees.append(TimeIntervalTree(intervals))

        return tuple(trees)
