# -*- encoding: utf-8 -*-
import collections
import copy
import fractions
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin \
	import TimeIntervalAggregateMixin


class TimeIntervalTree(TimeIntervalAggregateMixin):
    r'''An augmented red-black tree for storing and searching for intervals of
    time (rather than pitch).

    This allows for the arbitrary placement of blocks of material along a
    time-line.  While this functionality could be achieved with Python's
    built-in collections, this class reduces the complexity of the search
    process, such as locating overlapping intervals.

    TimeIntervalTrees can be instantiated without contents, or from a mixed
    collection of other TimeIntervalTrees and / or TimeIntervals.  The input
    will be parsed recursively:

    ::

        >>> from abjad.tools.timeintervaltools import *

    ::

        >>> interval_one = TimeInterval(0, 10)
        >>> interval_two = TimeInterval(1, 8)
        >>> interval_three = TimeInterval(3, 13)
        >>> tree = TimeIntervalTree(
        ...     [interval_one, interval_two, interval_three])

    ::

        >>> tree
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(10, 1), {}),
            TimeInterval(Offset(1, 1), Offset(8, 1), {}),
            TimeInterval(Offset(3, 1), Offset(13, 1), {})
        ])

    Return `TimeIntervalTree` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_root',
        '_sentinel',
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(self, intervals=None):
        from abjad.tools import timeintervaltools
        self._sentinel = timeintervaltools.TimeIntervalTreeNode(0)
        self._sentinel.red = True
        self._sentinel.left = self._sentinel
        self._sentinel.right = self._sentinel
        self._sentinel.parent = self._sentinel
        self._root = self._sentinel
        self._start = None
        self._stop = None
        if intervals is not None:
            self._insert(intervals)

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        if item in self._inorder:
            return True
        else:
            return False

    def __copy__(self):
        return type(self)([copy.copy(x) for x in self])

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self[:] == expr[:]:
                return True
        return False

    def __getitem__(self, item):
        return self._inorder.__getitem__(item)

    def __getslice__(self, start_offset, end):
        return self._inorder.__getslice__(start_offset, end)

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

    def __ne__(self, expr):
        return not self.__eq__(expr)

    def __nonzero__(self):
        '''`TimeIntervalTree` evaluates to True if it contains any intervals:

        ::

            >>> true_tree = TimeIntervalTree([TimeInterval(0, 1)])
            >>> false_tree = TimeIntervalTree([])

        ::

            >>> bool(true_tree)
            True
            >>> bool(false_tree)
            False

        Returns boolean.
        '''
        return bool(len(self))

    def __repr__(self):
        if self:
            intervals = [repr(interval) for interval in self._inorder]
            return '%s([\n\t%s\n])' % (
                self._class_name, ',\n\t'.join(intervals))
        else:
            return '%s([])' % self._class_name

    ### PRIVATE PROPERTIES ###

    @property
    def _inorder(self):
        if self:
            intervals = []
            nodes = tuple(self._sort_nodes_inorder())
            for node in nodes:
                intervals.extend(
                    sorted(node.payload, key=lambda x: x.signature))
            return tuple(intervals)
        else:
            return ()

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Absolute difference of the stop_offset and start_offset values of the tree:

        ::

            >>> ti1 = TimeInterval(1, 2)
            >>> ti2 = TimeInterval(3, (7, 2))
            >>> tree = TimeIntervalTree([ti1, ti2])
            >>> tree.duration
            Duration(5, 2)

        Empty trees have a duration of 0.

        Return ``Duration`` instance.
        '''
        if self:
            return durationtools.Duration(
                self.latest_stop - self.earliest_start)
        else:
            return durationtools.Duration(0)

    @property
    def earliest_start(self):
        r'''The minimum start_offset value of all intervals in the tree:

        ::

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
        r'''The minimum stop_offset value of all intervals in the tree:

        ::

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
    def intervals_are_contiguous(self):
        r'''True when all intervals are contiguous and non-overlapping,
        otherwise False.

        Returns boolean.
        '''
        for first, second in sequencetools.iterate_sequence_pairwise_strict(
            self):
            if first.stop_offset != second.start_offset:
                return False
        return True

    @property
    def intervals_are_nonoverlapping(self):
        r'''True when all intervals are non-overlapping, otherwise False.

        Returns boolean.
        '''
        for first, second in sequencetools.iterate_sequence_pairwise_strict(
            self):
            if second.start_offset < first.stop_offset:
                return False
        return True

    @property
    def latest_start(self):
        r'''The maximum start_offset value of all intervals in the tree:

        ::

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
        r'''The maximum stop_offset value of all intervals in the tree:

        ::

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

    def _delete_fixup(self, x):
        while x != self._root and not x.red:
            if x == x.parent.left:
                w = x.parent.right
                # case one
                if w.red:
                    w.red = False
                    x.parent.red = True
                    if x.parent.right != self._sentinel:
                        self._rotate_left(x.parent)
                        w = x.parent.right
                # case two
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.parent
                else:
                    # case three
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        if w.left != self._sentinel:
                            self._rotate_right(w)
                            w = x.parent.right
                    # case four
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    if x.parent != self._sentinel:
                        self._rotate_left(x.parent)
                    x = self._root
            else:
                w = x.parent.left
                # case one
                if w.red:
                    w.red = False
                    x.parent.red = True
                    if x.parent.left != self._sentinel:
                        self._rotate_right(x.parent)
                        w = x.parent.left
                # case two
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.parent
                else:
                    # case three
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        if w.right != self._sentinel:
                            self._rotate_left(w)
                            w = x.parent.left
                    # case four
                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    if x.parent != self._sentinel:
                        self._rotate_right(x.parent)
                    x = self._root
        x.red = False

    def _delete_node(self, z):
        if z.left == self._sentinel or z.right == self._sentinel:
            y = z
        else:
            y = self._find_successor(z)
        if y.left != self._sentinel:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent
        if y.parent == self._sentinel:
            self._root = x
        elif y.is_left_child:
            y.parent.left = x
        else:
            y.parent.right = x
        if y != z:
            z.key = y.key
            z.payload = y.payload
        if not y.red:
            self._delete_fixup(x)

    def _find_by_key(self, key):
        node = self._root
        while node != self._sentinel:
            if node.key == key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _find_maximum(self, node):
        while node.right != self._sentinel:
            node = node.right
        return node

    def _find_minimum(self, node):
        while node.left != self._sentinel:
            node = node.left
        return node

    def _find_predecessor(self, node):
        if node.left != self._sentinel:
            return self._find_maximum(node.left)
        parent = node.parent
        while parent != self._sentinel and node.is_left_child:
            node = parent
            parent = node.parent
        return parent

    def _find_successor(self, node):
        if node.right != self._sentinel:
            return self._find_minimum(node.right)
        parent = node.parent
        while parent != self._sentinel and node.is_right_child:
            node = parent
            parent = node.parent
        return parent

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
            node = self._find_by_key(interval.start_offset)
            if node is not None:
                node.payload.append(interval)
            else:
                node = timeintervaltools.TimeIntervalTreeNode(interval.start_offset, interval)
                node.left = self._sentinel
                node.right = self._sentinel
                node.parent = self._sentinel
                self._insert_node(node)
        self._update_stop_extrema()
        self._start = self.earliest_start
        self._stop = self.latest_stop

    def _insert_fixup(self, z):
        while z != self._root and z.parent.red:
            if z.parent.is_left_child:
                y = z.parent.parent.right
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z.is_right_child:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z.is_left_child:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._rotate_left(z.parent.parent)
        self._root.red = False

    def _insert_node(self, z):
        y = self._sentinel
        x = self._root
        while x != self._sentinel:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self._sentinel:
            self._root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = z.right = self._sentinel
        z.red = True
        self._insert_fixup(z)

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self._sentinel:
            y.left.parent = x
        if y != self._sentinel:
            y.parent = x.parent
        if x.parent == self._sentinel:
            self._root = y
        elif x != self._sentinel:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        if x != self._sentinel:
            x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self._sentinel:
            y.right.parent = x
        if y != self._sentinel:
            y.parent = x.parent
        if x.parent == self._sentinel:
            self._root = y
        elif x != self._sentinel:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        y.right = x
        if x != self._sentinel:
            x.parent = y

    def _sort_nodes_inorder(self):
        def recurse(node):
            nodes = []
            if node.left != self._sentinel:
                nodes.extend(recurse(node.left))
            nodes.append(node)
            if node.right != self._sentinel:
                nodes.extend(recurse(node.right))
            return nodes
        if self._root != self._sentinel:
            return recurse(self._root)
        else:
            return []

    def _update_stop_extrema(self):
        def recurse(node):
            max = min = node.payload[0].stop_offset
            for interval in node.payload[1:]:
                if max < interval.stop_offset:
                    max = interval.stop_offset
                if interval.stop_offset < min:
                    min = interval.stop_offset
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

    def clip_interval_durations_to_range(self, minimum=None, maximum=None):
        from abjad.tools import timeintervaltools
        if not self:
            return self
        if minimum is not None:
            minimum = durationtools.Duration(minimum)
            assert 0 < minimum
        if maximum is not None:
            maximum = durationtools.Duration(maximum)
            assert 0 < maximum
        if minimum is not None and maximum is not None:
            assert minimum < maximum
        intervals = []
        for interval in self:
            if minimum is not None and interval.duration < minimum:
                intervals.append(interval.scale_to_rational(minimum))
            elif maximum is not None and maximum < interval.duration:
                intervals.append(interval.scale_to_rational(maximum))
            else:
                intervals.append(interval)
        return timeintervaltools.TimeIntervalTree(intervals)

    def explode_intervals(self, aggregate_count=None):
        r'''Explode intervals into trees, avoiding overlap and distributing
        density.

        ::

            >>> tree = timeintervaltools.TimeIntervalTree(
            ...     timeintervaltools.make_test_intervals())
            >>> tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
                TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
                TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
                TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
                TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
                TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
                TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
                TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
                TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
                TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'}),
                TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
            ])

        ..  container:: example

            **Example 1.** Explode intervals into optimal number of non-overlapping trees:

            ::

                >>> exploded_trees = tree.explode_intervals()
                >>> for exploded_tree in exploded_trees:
                ...     exploded_tree
                ...
                TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
                    TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
                    TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
                    TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
                    TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
                    TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
                    TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
                    TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
                    TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                    TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
                ])

        ..  container:: example

            **Example 2.** Explode intervals into less-than-optimal number of overlapping
            trees:

            ::

                >>> exploded_trees = tree.explode_intervals(aggregate_count=2)
                >>> for exploded_tree in exploded_trees:
                ...     exploded_tree
                ...
                TimeIntervalTree([
                    TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
                    TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
                    TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
                    TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                    TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
                    TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
                    TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
                    TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
                    TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
                    TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
                    TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
                ])

        ..  container:: example

            **Example 3.** Explode intervals into greater-than-optimal number of 
            non-overlapping trees:

            ::

                >>> exploded_trees = tree.explode_intervals(aggregate_count=6)
                >>> for exploded_tree in exploded_trees:
                ...     exploded_tree
                ...
                TimeIntervalTree([
                    TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
                    TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
                    TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
                    TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
                    TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'})
                ])
                TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
                    TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
                    TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
                ])

        Returns 0 or more trees.
        '''
        from abjad.tools import timeintervaltools

        assert isinstance(aggregate_count, (type(None), int))
        if isinstance(aggregate_count, int):
            assert 0 < aggregate_count

        if not len(self):
            return []

        bounding_interval = timeintervaltools.TimeInterval(
            self.start_offset, self.stop_offset)
        global_densities = []
        empty_tree_pairs = []
        exploded_trees = []
        if aggregate_count is not None:
            for i in xrange(aggregate_count):
                global_densities.append(0)
                exploded_tree = timeintervaltools.TimeIntervalTree()
                empty_tree_pairs.append((i, exploded_tree))
                exploded_trees.append(exploded_tree)

        for current_interval in self:

            if empty_tree_pairs:
                i, empty_tree = empty_tree_pairs.pop()
                empty_tree._insert(current_interval)
                global_densities[i] = empty_tree.calculate_depth_density(
                    bounding_interval=bounding_interval)
                continue
                
            nonoverlapping_trees = []
            overlapping_trees = []
            for i, exploded_tree in enumerate(exploded_trees):
                local_density = exploded_tree.calculate_depth_density(
                    bounding_interval=current_interval)
                global_density = global_densities[i]
                if not local_density:
                    nonoverlapping_trees.append((i, global_density)) 
                else:
                    overlapping_trees.append((i, local_density, global_density))
            nonoverlapping_trees.sort(key=lambda x: x[1])
            overlapping_trees.sort(key=lambda x: (x[1], x[2]))

            if not nonoverlapping_trees and aggregate_count is None:
                exploded_tree = timeintervaltools.TimeIntervalTree(
                    [current_interval])
                global_densities.append(exploded_tree.calculate_depth_density(
                    bounding_interval=bounding_interval))
                exploded_trees.append(exploded_tree)
                continue

            if nonoverlapping_trees:
                i = nonoverlapping_trees[0][0]
            else:
                i = overlapping_trees[0][0]
            exploded_tree = exploded_trees[i]
            global_densities[i] = exploded_tree.calculate_depth_density(
                bounding_interval=bounding_interval)
            exploded_tree._insert(current_interval)

        return tuple(exploded_trees)
        
    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        r'''Find all intervals in tree intersecting or tangent to the interval
        defined in `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval(0, 1)
            >>> found = \
            ...     tree.find_intervals_intersecting_or_tangent_to_interval(
            ...     interval)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c']

        ::

            >>> interval = TimeInterval(3, 4)
            >>> found = \
            ...     tree.find_intervals_intersecting_or_tangent_to_interval(
            ...     interval)
            >>> sorted([x['name'] for x in found])
            ['c', 'd']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools
        def recurse(node, start_offset, stop_offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if node.key <= stop_offset and start_offset <= node.latest_stop:
                for interval in node.payload:
                    if interval.start_offset <= stop_offset and start_offset <= interval.stop_offset:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and self._find_minimum(node.left).key <= stop_offset \
                and start_offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, start_offset, stop_offset))
            if node.right != self._sentinel \
                and self._find_minimum(node.right).key <= stop_offset \
                and start_offset <= node.right.latest_stop:
                intervals.extend(recurse(node.right, start_offset, stop_offset))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start_offset, stop_offset = args[0].start_offset, args[0].stop_offset
        elif len(args) == 2:
            start_offset, stop_offset = args[0], args[1]
            assert all(isinstance(x, (int, Fraction)) for x in (start_offset, stop_offset))
            assert start_offset <= stop_offset
        else:
            raise ValueError
        return type(self)(recurse(self._root, start_offset, stop_offset))

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        r'''Find all intervals in tree intersecting or tangent to `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 1
            >>> found = \
            ...     tree.find_intervals_intersecting_or_tangent_to_offset(
            ...     offset)
            >>> sorted([x['name'] for x in found])
            ['a', 'b', 'c']

        ::

            >>> offset = 3
            >>> found = \
            ...     tree.find_intervals_intersecting_or_tangent_to_offset(
            ...     offset)
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
                    if interval.start_offset <= offset and offset <= interval.stop_offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                self._find_minimum(node.left).key <= offset and \
                offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and \
                self._find_minimum(node.right).key <= offset and \
                offset <= node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_after_offset(self, offset):
        r'''Find all intervals in tree starting after `offset`:

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
            if node.left != self._sentinel and \
                offset < self._find_maximum(node.left).key:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        r'''Find all intervals in tree starting and stopping within the interval
        defined by `args`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> interval = TimeInterval(1, 3)
            >>> found = \
            ...     tree.find_intervals_starting_and_stopping_within_interval(
            ...     interval)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        ::

            >>> interval = TimeInterval(-1, 2)
            >>> found = \
            ...     tree.find_intervals_starting_and_stopping_within_interval(
            ...     interval)
            >>> sorted([x['name'] for x in found])
            ['a', 'b']

        Return `TimeIntervalTree` instance.
        '''
        from abjad.tools import timeintervaltools
        def recurse(node, start_offset, stop_offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start_offset <= node.key and node.earliest_stop <= stop_offset:
                for interval in node.payload:
                    if start_offset <= interval.start_offset and interval.stop_offset <= stop_offset:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and start_offset <= self._find_maximum(node.left).key \
                and node.left.earliest_stop <= stop_offset:
                intervals.extend(recurse(node.left, start_offset, stop_offset))
            if node.right != self._sentinel \
                and start_offset <= self._find_maximum(node.right).key \
                and node.right.earliest_stop <= stop_offset:
                intervals.extend(recurse(node.right, start_offset, stop_offset))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start_offset, stop_offset = args[0].start_offset, args[0].stop_offset
        elif len(args) == 2:
            start_offset, stop_offset = args[0], args[1]
            assert all(isinstance(x, (int, Fraction)) for x in (start_offset, stop_offset))
            assert start_offset <= stop_offset
        else:
            raise ValueError
        return type(self)(recurse(self._root, start_offset, stop_offset))

    def find_intervals_starting_at_offset(self, offset):
        r'''Find all intervals in tree starting at `offset`:

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
        r'''Find all intervals in tree starting before `offset`:

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
            if node.right != self._sentinel and \
                self._find_minimum(node.right).key < offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        r'''Find all intervals in tree starting or stopping at `offset`:

        ::

            >>> a = TimeInterval(0, 1, {'name': 'a'})
            >>> b = TimeInterval(1, 2, {'name': 'b'})
            >>> c = TimeInterval(0, 3, {'name': 'c'})
            >>> d = TimeInterval(2, 3, {'name': 'd'})
            >>> tree = TimeIntervalTree([a, b, c, d])

        ::

            >>> offset = 2
            >>> found = \
            ...     tree.find_intervals_starting_or_stopping_at_offset(offset)
            >>> sorted([x['name'] for x in found])
            ['b', 'd']

        ::

            >>> offset = 1
            >>> found = \
            ...     tree.find_intervals_starting_or_stopping_at_offset(offset)
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
                    if interval.start_offset == offset or interval.stop_offset == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and \
                self._find_minimum(node.right).key <= offset \
                and offset <= node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_starting_within_interval(self, *args):
        r'''Find all intervals in tree starting within the interval defined 
        by `args`:

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
        def recurse(node, start_offset, stop_offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start_offset <= node.key <= stop_offset:
                intervals.extend(node.payload)
            if node.left != self._sentinel and \
                start_offset <= self._find_maximum(node.left).key and \
                self._find_minimum(node.left).key <= stop_offset:
                intervals.extend(recurse(node.left, start_offset, stop_offset))
            if node.right != self._sentinel and \
                start_offset <= self._find_maximum(node.right).key and \
                self._find_minimum(node.right).key <= stop_offset:
                intervals.extend(recurse(node.right, start_offset, stop_offset))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start_offset, stop_offset = args[0].start_offset, args[0].stop_offset
        elif len(args) == 2:
            start_offset, stop_offset = args[0], args[1]
            assert all(isinstance(x, (int, Fraction)) for x in (start_offset, stop_offset))
            assert start_offset <= stop_offset
        else:
            raise ValueError
        return type(self)(recurse(self._root, start_offset, stop_offset))

    def find_intervals_stopping_after_offset(self, offset):
        r'''Find all intervals in tree stopping after `offset`:

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
                    if offset < interval.stop_offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                offset < node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and \
                offset < node.right.latest_stop:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_at_offset(self, offset):
        r'''Find all intervals in tree stopping at `offset`:

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
                    if interval.stop_offset == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                offset <= node.left.latest_stop:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and \
                node.right.earliest_stop <= offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_before_offset(self, offset):
        r'''Find all intervals in tree stopping before `offset`:

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
                    if interval.stop_offset < offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                node.left.earliest_stop < offset:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and \
                node.right.earliest_stop < offset:
                intervals.extend(recurse(node.right, offset))
            return intervals

        offset = durationtools.Offset(offset)
        return type(self)(recurse(self._root, offset))

    def find_intervals_stopping_within_interval(self, *args):
        r'''Find all intervals in tree stopping within the interval 
        defined by `args`:

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
        def recurse(node, start_offset, stop_offset):
            intervals = []
            if node == self._sentinel:
                return intervals
            if start_offset <= node.latest_stop and node.earliest_stop <= stop_offset:
                for interval in node.payload:
                    if start_offset <= interval.stop_offset <= stop_offset:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                start_offset <= node.left.latest_stop and \
                node.left.earliest_stop <= stop_offset:
                intervals.extend(recurse(node.left, start_offset, stop_offset))
            if node.right != self._sentinel and \
                start_offset <= node.right.latest_stop and \
                node.right.earliest_stop <= stop_offset:
                intervals.extend(recurse(node.right, start_offset, stop_offset))
            return intervals

        if len(args) == 1:
            assert isinstance(args[0], timeintervaltools.TimeIntervalMixin)
            start_offset, stop_offset = args[0].start_offset, args[0].stop_offset
        elif len(args) == 2:
            start_offset, stop_offset = args[0], args[1]
            assert all(isinstance(x, (int, Fraction)) for x in (start_offset, stop_offset))
            assert start_offset <= stop_offset
        else:
            raise ValueError

        return type(self)(recurse(self._root, start_offset, stop_offset))

    def fuse_overlapping_intervals(self, include_tangent_intervals=False):
        r'''Fuse overlapping intervals:

        ::

            >>> a = TimeInterval(0, 10)
            >>> b = TimeInterval(5, 15)
            >>> c = TimeInterval(15, 25)
            >>> tree = TimeIntervalTree([a, b, c])
            >>> tree.fuse_overlapping_intervals()
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(15, 1), {}),
                TimeInterval(Offset(15, 1), Offset(25, 1), {})
            ])

        ::
        
            >>> tree.fuse_overlapping_intervals(include_tangent_intervals=True)
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(25, 1), {})
            ])

        Returns time interval tree.
        '''
        from abjad.tools import timeintervaltools
        trees = [timeintervaltools.TimeIntervalTree(group) for group in
            self.partition(
                include_tangent_intervals=include_tangent_intervals)]
        return timeintervaltools.TimeIntervalTree([
            timeintervaltools.TimeInterval(
                tree.earliest_start,
                tree.latest_stop,
                )
            for tree in trees
            ])

    def quantize_to_rational(self, rational):
        r'''Quantize all intervals in tree to a multiple (1 or more) 
        of `rational`:

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
        assert 0 < rational
        intervals = []
        for interval in self:
            start_offset = durationtools.Offset(
                int(round(interval.start_offset / rational))) * rational
            stop_offset = durationtools.Offset(
                int(round(interval.stop_offset / rational))) * rational
            if start_offset == stop_offset:
                stop_offset = start_offset + rational
            intervals.append(
                interval.shift_to_rational(start_offset).scale_to_rational(
                    stop_offset - start_offset))
        return type(self)(intervals)

    def scale_by_rational(self, rational):
        r'''Scale aggregate duration of tree by `rational`:

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

        Scaling works regardless of the starting offset of 
        the `TimeIntervalTree`:

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

            >>> result.start_offset == tree.start_offset
            True
            >>> result.duration == tree.duration * 2
            True

        Return `TimeIntervalTree` instance.
        '''
        rational = durationtools.Duration(rational)
        return type(self)([
            x.shift_to_rational(
                ((x.start_offset - self.start_offset) * rational) + self.start_offset).scale_by_rational(rational)
                for x in self
        ])

    def scale_interval_durations_by_rational(self, rational):
        r'''Scale the duration of each interval by
        `rational`, maintaining their start_offset offsets:

        ::

            >>> a = timeintervaltools.TimeInterval(-1, 3)
            >>> b = timeintervaltools.TimeInterval(6, 12)
            >>> c = timeintervaltools.TimeInterval(9, 16)
            >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
            >>> tree.scale_interval_durations_by_rational(Multiplier(6, 5))
            TimeIntervalTree([
                TimeInterval(Offset(-1, 1), Offset(19, 5), {}),
                TimeInterval(Offset(6, 1), Offset(66, 5), {}),
                TimeInterval(Offset(9, 1), Offset(87, 5), {})
            ])

        Returns TimeIntervalTree.
        '''
        from abjad.tools import timeintervaltools
        rational = durationtools.Multiplier(rational)
        assert 0 < rational
        if not self or rational == 1:
            return self
        return timeintervaltools.TimeIntervalTree([
            x.scale_by_rational(rational)
            for x in self
            ])

    def scale_interval_durations_to_rational(self, rational):
        r'''Scale the duration of each interval to
        `rational`, maintaining their start_offset offsets:

        ::

            >>> a = timeintervaltools.TimeInterval(-1, 3)
            >>> b = timeintervaltools.TimeInterval(6, 12)
            >>> c = timeintervaltools.TimeInterval(9, 16)
            >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
            >>> tree.scale_interval_durations_to_rational(Duration(1, 7))
            TimeIntervalTree([
                TimeInterval(Offset(-1, 1), Offset(-6, 7), {}),
                TimeInterval(Offset(6, 1), Offset(43, 7), {}),
                TimeInterval(Offset(9, 1), Offset(64, 7), {})
            ])

        Returns TimeIntervalTree.
        '''
        from abjad.tools import timeintervaltools
        rational = durationtools.Duration(rational)
        assert 0 < rational
        if not self:
            return self
        return timeintervaltools.TimeIntervalTree([
            x.scale_to_rational(rational) 
            for x in self
            ])

    def scale_interval_offsets_by_rational(self, rational):
        r'''Scale the starting offset of each interval by
        `rational`, maintaining the earliest startest offset:

        ::

            >>> a = timeintervaltools.TimeInterval(-1, 3)
            >>> b = timeintervaltools.TimeInterval(6, 12)
            >>> c = timeintervaltools.TimeInterval(9, 16)
            >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
            >>> tree.scale_interval_offsets_by_rational(Multiplier(4, 5))
            TimeIntervalTree([
                TimeInterval(Offset(-1, 1), Offset(3, 1), {}),
                TimeInterval(Offset(23, 5), Offset(53, 5), {}),
                TimeInterval(Offset(7, 1), Offset(14, 1), {})
            ])

        Returns interval tree.
        '''
        from abjad.tools import timeintervaltools
        rational = durationtools.Multiplier(rational)
        assert 0 < rational
        if not self or rational == 1:
            return self
        return timeintervaltools.TimeIntervalTree([
            x.shift_to_rational(
                ((x.start_offset - self.start_offset) * rational) 
                + self.start_offset)
                for x in self
            ])

    def scale_to_rational(self, rational):
        r'''Scale aggregate duration of tree to `rational`:

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

        Scaling works regardless of the starting offset of 
        the `TimeIntervalTree`:

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
                ((x.start_offset - self.start_offset) * ratio) + self.start_offset).scale_by_rational(ratio)
                for x in self])

    def shift_by_rational(self, rational):
        r'''Shift aggregate offset of tree by `rational`:

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
        r'''Shift aggregate offset of tree to `rational`:

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
            x.shift_by_rational(rational - self.start_offset) for x in self
        ])

    def split_at_rationals(self, *rationals):
        r'''Split tree at each rational in `rationals`:

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

        Returns tuple of `TimeIntervalTree` instances.
        '''
        assert 0 < len(rationals)
        rationals = sorted([durationtools.Offset(x) for x in rationals])
        rationals = [x for x in rationals if self.start_offset < x < self.stop_offset]
        trees = []
        intervals = self[:]
        before = []
        after = []
        for rational in rationals:
            for interval in intervals:
                splits = interval.split_at_rationals(rational)
                if len(splits) == 1:
                    if splits[0].stop_offset <= rational:
                        before.append(splits[0])
                    elif rational <= splits[0].start_offset:
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
