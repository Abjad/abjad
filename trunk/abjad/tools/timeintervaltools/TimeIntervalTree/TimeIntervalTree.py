import collections
import copy
import fractions
from abjad.tools import durationtools
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin import TimeIntervalAggregateMixin
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
    will be parsed recursively:

    ::

        >>> from abjad.tools.timeintervaltools import TimeIntervalTree
        >>> from abjad.tools.timeintervaltools import TimeInterval

    ::

        >>> interval_one = TimeInterval(0, 10)
        >>> interval_two = TimeInterval(1, 8)
        >>> interval_three = TimeInterval(3, 13)
        >>> tree = TimeIntervalTree([interval_one, interval_two, interval_three])

    ::

        >>> tree
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(10, 1), {}),
            TimeInterval(Offset(1, 1), Offset(8, 1), {}),
            TimeInterval(Offset(3, 1), Offset(13, 1), {})
        ])

    Return `TimeIntervalTree` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_root', '_sentinel', '_start', '_stop')

    ### INITIALIZER ###

    def __init__(self, intervals=None):
        from abjad.tools.timeintervaltools._IntervalNode._IntervalNode import _IntervalNode
        self._sentinel = _IntervalNode(0)
        self._sentinel.red = True
        self._sentinel.left = self._sentinel
        self._sentinel.right = self._sentinel
        self._sentinel.parent = self._sentinel
        self._root = self._sentinel
        if intervals is not None:
            self._insert(intervals)
        self._start = self.earliest_start
        self._stop = self.latest_stop

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        if item in self._inorder:
            return True
        else:
            return False

    def __copy__(self):
        return type(self)([copy.copy(x) for x in self])

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

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        '''`TimeIntervalTree` evaluates to True if it contains any intervals:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> true_tree = TimeIntervalTree([TimeInterval(0, 1)])
            >>> false_tree = TimeIntervalTree([])

        ::

            >>> bool(true_tree)
            True
            >>> bool(false_tree)
            False

        Return boolean.
        '''
        return bool(len(self))

    def __repr__(self):
        if self:
            intervals = [repr(interval) for interval in self._inorder]
            return '%s([\n\t%s\n])' % (type(self).__name__, ',\n\t'.join(intervals))
        else:
            return '%s([])' % type(self).__name__

    ### PRIVATE PROPERTIES ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Absolute difference of the stop and start values of the tree:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.duration
            Duration(5, 2)

        Empty trees have a duration of 0.

        Return ``Duration`` instance.
        '''
        if self:
            return durationtools.Duration(self.latest_stop - self.earliest_start)
        else:
            return durationtools.Duration(0)

    @property
    def earliest_start(self):
        '''The minimum start value of all intervals in the tree:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.earliest_start
            Offset(1, 1)

        Return ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return durationtools.Offset(self._find_minimum(self._root).key)
        else:
            return None

    @property
    def earliest_stop(self):
        '''The minimum stop value of all intervals in the tree:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.earliest_stop
            Offset(2, 1)

        Return ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return durationtools.Offset(self._root.earliest_stop)
        else:
            return None

    @property
    def intervals(self):
        return tuple(self[:])

    @property
    def latest_start(self):
        '''The maximum start value of all intervals in the tree:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.latest_start
            Offset(3, 1)

        Return ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return durationtools.Offset(self._find_maximum(self._root).key)
        else:
            return None

    @property
    def latest_stop(self):
        '''The maximum stop value of all intervals in the tree:

        ::

            >>> from abjad.tools.timeintervaltools import *
            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.latest_stop
            Offset(7, 2)

        Return ``Offset`` instance, or None if tree is empty.
        '''
        if self:
            return durationtools.Offset(self._root.latest_stop)
        else:
            return None

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        if not len(self):
            return ['{}()'.format(self._tools_package_qualified_class_name)]
        pieces = []
        pieces.append('{}(['.format(self._tools_package_qualified_class_name))
        for interval in self:
            ipieces = interval._get_tools_package_qualified_repr_pieces()
            if 1 < len(ipieces):
                for ipiece in ipieces[:-1]:
                    pieces.append('\t{}'.format(ipiece))
                pieces.append('\t{},'.format(ipieces[-1]))
            else:
                pieces.append('\t{},'.format(ipieces[0]))
        pieces.append('\t])')
        return pieces

    def _insert(self, args):
        from abjad.tools import timeintervaltools
        from abjad.tools.timeintervaltools._IntervalNode._IntervalNode import _IntervalNode

        def recurse(x):
            result = []
            if isinstance(x, timeintervaltools.TimeInterval):
                result.append(x)
            elif isinstance(x, timeintervaltools.TimeIntervalAggregateMixin):
                result.extend(x.intervals)
            elif isinstance(x, collections.Iterable) and \
                not isinstance(x, (basestring)):
                for y in x:
                    result.extend(recurse(y))
            return result

        intervals = recurse([args])

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
        '''Find all intervals in tree intersecting or tangent to the interval
        defined in `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval(0, 1)
            >>> found = tree.find_intervals_intersecting_or_tangent_to_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c']

        ::

            >>> interval = TimeInterval(3, 4)
            >>> found = tree.find_intervals_intersecting_or_tangent_to_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools

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
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError

        return type(self)(recurse(self._root, start, stop))

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        '''Find all intervals in tree intersecting or tangent to `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_intersecting_or_tangent_to_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c']

        ::

            >>> offset = 3
            >>> found = tree.find_intervals_intersecting_or_tangent_to_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_after_offset(self, offset):
        '''Find all intervals in tree starting after `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 0
            >>> found = tree.find_intervals_starting_after_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_starting_after_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['d']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        '''Find all intervals in tree starting and stopping within the interval
        defined by `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval(1, 3)
            >>> found = tree.find_intervals_starting_and_stopping_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        ::

            >>> interval = TimeInterval(-1, 2)
            >>> found = tree.find_intervals_starting_and_stopping_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['a', 'b']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools

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
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError

        return type(self)(recurse(self._root, start, stop))

    def find_intervals_starting_at_offset(self, offset):
        '''Find all intervals in tree starting at `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 0
            >>> found = tree.find_intervals_starting_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'c']

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_starting_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['b']

        Return `TimeIntervalTree` instance.
        '''

        offset = durationtools.Offset(offset)
        node = self._find_by_key(offset)
        intervals = []
        if node is not None and node != self._sentinel:
            intervals = node.payload
        return type(self)(intervals)

    def find_intervals_starting_before_offset(self, offset):
        '''Find all intervals in tree starting before `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_starting_before_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'c']

        ::

            >>> offset = 2
            >>> found = tree.find_intervals_starting_before_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        '''Find all intervals in tree starting or stopping at `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 2 
            >>> found = tree.find_intervals_starting_or_stopping_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_starting_or_stopping_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_within_interval(self, *args):
        '''Find all intervals in tree starting within the interval defined by
        `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval((-1, 2), (1, 2))
            >>> found = tree.find_intervals_starting_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['a', 'c']

        ::

            >>> interval = TimeInterval((1, 2), (5, 2))
            >>> found = tree.find_intervals_starting_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools

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
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError

        return type(self)(recurse(self._root, start, stop))

    def find_intervals_stopping_after_offset(self, offset):
        '''Find all intervals in tree stopping after `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_stopping_after_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['b', 'c', 'd']

        ::

            >>> offset = 2
            >>> found = tree.find_intervals_stopping_after_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_at_offset(self, offset):
        '''Find all intervals in tree stopping at `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 3
            >>> found = tree.find_intervals_stopping_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        ::

            >>> offset = 1
            >>> found = tree.find_intervals_stopping_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_before_offset(self, offset):
        '''Find all intervals in tree stopping before `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 3
            >>> found = tree.find_intervals_stopping_before_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b']

        ::

            >>> offset = (7, 2)
            >>> found = tree.find_intervals_stopping_before_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c', 'd']

        Return `TimeIntervalTree` instance.
        '''

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

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_within_interval(self, *args):
        '''Find all intervals in tree stopping within the interval defined by `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval((3, 2), (5, 2))
            >>> found = tree.find_intervals_stopping_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['b']

        ::

            >>> interval = TimeInterval((5, 2), (7, 2))
            >>> found = tree.find_intervals_stopping_within_interval(interval)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools

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
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start, stop = args[0].start, args[0].stop
        elif len(args) == 2:
            start, stop = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (start, stop)])
            assert start <= stop
        else:
            raise ValueError

        return type(self)(recurse(self._root, start, stop))

    def quantize_to_rational(self, rational):
        '''Quantize all intervals in tree to a multiple (1 or more) of `rational`:

        ::

            >>> a = TimeInterval((1, 16), (1, 8), {'name': 'a'})
            >>> b = TimeInterval((2, 7), (13, 7), {'name': 'b'})
            >>> c = TimeInterval((3, 5), (8, 5), {'name': 'c'})
            >>> d = TimeInterval((2, 3), (5, 3), {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(1, 16), Offset(1, 8), {'name': 'a'}),
                TimeInterval(Offset(2, 7), Offset(13, 7), {'name': 'b'}),
                TimeInterval(Offset(3, 5), Offset(8, 5), {'name': 'c'}),
                TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'd'})
            ])

        ::

            >>> rational = (1, 4)
            >>> tree.quantize_to_rational(rational)
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 4), {'name': 'a'}),
                TimeInterval(Offset(1, 4), Offset(7, 4), {'name': 'b'}),
                TimeInterval(Offset(1, 2), Offset(3, 2), {'name': 'c'}),
                TimeInterval(Offset(3, 4), Offset(7, 4), {'name': 'd'})
            ])

        ::

            >>> rational = (1, 3)
            >>> tree.quantize_to_rational(rational)
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 3), {'name': 'a'}),
                TimeInterval(Offset(1, 3), Offset(2, 1), {'name': 'b'}),
                TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'c'}),
                TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'd'})
            ])

        Return `TimeIntervalTree` instance.
        '''

        rational = durationtools.Duration(rational)
        intervals = []
        for interval in self:
            start = durationtools.Offset(int(round(interval.start / rational))) * rational
            stop = durationtools.Offset(int(round(interval.stop / rational))) * rational
            if start == stop:
                stop = start + rational
            intervals.append(interval.shift_to_rational(start).scale_to_rational(stop - start))
        return type(self)(intervals)

    def scale_by_rational(self, rational):
        '''Scale aggregate duration of tree by `rational`:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> from abjad.tools.timeintervaltools import TimeIntervalTree

        ::

            >>> one = TimeInterval(0, 1, {'name': 'one'})
            >>> two = TimeInterval((1, 2), (5, 2), {'name': 'two'})
            >>> three = TimeInterval(2, 4, {'name': 'three'})
            >>> tree = TimeIntervalTree([one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.scale_by_rational((2, 3))
            >>> result
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(2, 3), {'name': 'one'}),
                TimeInterval(Offset(1, 3), Offset(5, 3), {'name': 'two'}),
                TimeInterval(Offset(4, 3), Offset(8, 3), {'name': 'three'})
            ])

        Scaling works regardless of the starting offset of the `TimeIntervalTree`:

        ::

            >>> zero = TimeInterval(-4, 0, {'name': 'zero'})
            >>> tree = TimeIntervalTree([zero, one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(-4, 1), Offset(0, 1), {'name': 'zero'}),
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.scale_by_rational(2)
            >>> result
            TimeIntervalTree([
                TimeInterval(Offset(-4, 1), Offset(4, 1), {'name': 'zero'}),
                TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 'one'}),
                TimeInterval(Offset(5, 1), Offset(9, 1), {'name': 'two'}),
                TimeInterval(Offset(8, 1), Offset(12, 1), {'name': 'three'})
            ])

        ::

            >>> result.start == tree.start
            True
            >>> result.duration == tree.duration * 2
            True

        Return `TimeIntervalTree` instance.
        '''

        rational = durationtools.Duration(rational)
        return type(self)([
            x.shift_to_rational(
                ((x.start - self.start) * rational) + self.start).scale_by_rational(rational)\
                for x in self
        ])

    def scale_to_rational(self, rational):
        '''Scale aggregate duration of tree to `rational`:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> from abjad.tools.timeintervaltools import TimeIntervalTree

        ::

            >>> one = TimeInterval(0, 1, {'name': 'one'})
            >>> two = TimeInterval((1, 2), (5, 2), {'name': 'two'})
            >>> three = TimeInterval(2, 4, {'name': 'three'})
            >>> tree = TimeIntervalTree([one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.scale_to_rational(1)
            >>> result
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 4), {'name': 'one'}),
                TimeInterval(Offset(1, 8), Offset(5, 8), {'name': 'two'}),
                TimeInterval(Offset(1, 2), Offset(1, 1), {'name': 'three'})
            ])

        ::

            >>> result.scale_to_rational(10)
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(5, 2), {'name': 'one'}),
                TimeInterval(Offset(5, 4), Offset(25, 4), {'name': 'two'}),
                TimeInterval(Offset(5, 1), Offset(10, 1), {'name': 'three'})
            ])

        Scaling works regardless of the starting offset of the `TimeIntervalTree`:

        ::

            >>> zero = TimeInterval(-4, 0, {'name': 'zero'})
            >>> tree = TimeIntervalTree([zero, one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(-4, 1), Offset(0, 1), {'name': 'zero'}),
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> tree.scale_to_rational(4)
            TimeIntervalTree([
                TimeInterval(Offset(-4, 1), Offset(-2, 1), {'name': 'zero'}),
                TimeInterval(Offset(-2, 1), Offset(-3, 2), {'name': 'one'}),
                TimeInterval(Offset(-7, 4), Offset(-3, 4), {'name': 'two'}),
                TimeInterval(Offset(-1, 1), Offset(0, 1), {'name': 'three'})
            ])

        Return `TimeIntervalTree` instance.
        '''

        rational = durationtools.Duration(rational)
        ratio = rational / self.duration
        return type(self)([
            x.shift_to_rational(
                ((x.start - self.start) * ratio) + self.start).scale_by_rational(ratio) \
                for x in self])

    def shift_by_rational(self, rational):
        '''Shift aggregate offset of tree by `rational`:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> from abjad.tools.timeintervaltools import TimeIntervalTree

        ::

            >>> one = TimeInterval(0, 1, {'name': 'one'})
            >>> two = TimeInterval((1, 2), (5, 2), {'name': 'two'})
            >>> three = TimeInterval(2, 4, {'name': 'three'})
            >>> tree = TimeIntervalTree([one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.shift_by_rational(-2.5)
            >>> result
            TimeIntervalTree([
                TimeInterval(Offset(-5, 2), Offset(-3, 2), {'name': 'one'}),
                TimeInterval(Offset(-2, 1), Offset(0, 1), {'name': 'two'}),
                TimeInterval(Offset(-1, 2), Offset(3, 2), {'name': 'three'})
            ])
            >>> result.shift_by_rational(6)
            TimeIntervalTree([
                TimeInterval(Offset(7, 2), Offset(9, 2), {'name': 'one'}),
                TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 'two'}),
                TimeInterval(Offset(11, 2), Offset(15, 2), {'name': 'three'})
            ])

        Return `TimeIntervalTree` instance.
        '''

        rational = durationtools.Offset(rational)
        return type(self)([
            x.shift_by_rational(rational) for x in self
        ])

    def shift_to_rational(self, rational):
        '''Shift aggregate offset of tree to `rational`:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> from abjad.tools.timeintervaltools import TimeIntervalTree

        ::

            >>> one = TimeInterval(0, 1, {'name': 'one'})
            >>> two = TimeInterval((1, 2), (5, 2), {'name': 'two'})
            >>> three = TimeInterval(2, 4, {'name': 'three'})
            >>> tree = TimeIntervalTree([one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.shift_to_rational(100)
            >>> result
            TimeIntervalTree([
                TimeInterval(Offset(100, 1), Offset(101, 1), {'name': 'one'}),
                TimeInterval(Offset(201, 2), Offset(205, 2), {'name': 'two'}),
                TimeInterval(Offset(102, 1), Offset(104, 1), {'name': 'three'})
            ])

        Return `TimeIntervalTree` instance.
        '''

        rational = durationtools.Offset(rational)
        return type(self)([
            x.shift_by_rational(rational - self.start) for x in self
        ])

    def split_at_rationals(self, *rationals):
        '''Split tree at each rational in `rationals`:

        ::

            >>> from abjad.tools.timeintervaltools import TimeInterval
            >>> from abjad.tools.timeintervaltools import TimeIntervalTree

        ::

            >>> one = TimeInterval(0, 1, {'name': 'one'})
            >>> two = TimeInterval((1, 2), (5, 2), {'name': 'two'})
            >>> three = TimeInterval(2, 4, {'name': 'three'})
            >>> tree = TimeIntervalTree([one, two, three])
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'})
            ])

        ::

            >>> result = tree.split_at_rationals(1, 2, 3)
            >>> len(result)
            4

        ::

            >>> result[0]
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                TimeInterval(Offset(1, 2), Offset(1, 1), {'name': 'two'})
            ])

        ::

            >>> result[1]
            TimeIntervalTree([
                TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'two'})
            ])

        ::

            >>> result[2]
            TimeIntervalTree([
                TimeInterval(Offset(2, 1), Offset(5, 2), {'name': 'two'}),
                TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'three'})
            ])

        ::

            >>> result[3]
            TimeIntervalTree([
                TimeInterval(Offset(3, 1), Offset(4, 1), {'name': 'three'})
            ])

        Return tuple of `TimeIntervalTree` instances.
        '''

        assert 0 < len(rationals)
        rationals = sorted([durationtools.Offset(x) for x in rationals])
        rationals = [x for x in rationals if self.start < x < self.stop]

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
                trees.append(type(self)(before))

            intervals = after
            before = []
            after = []

        if intervals:
            trees.append(type(self)(intervals))

        return tuple(trees)
