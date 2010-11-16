from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools._IntervalNode import _IntervalNode
from abjad.tools.treetools._RedBlackTree import _RedBlackTree


class IntervalTree(_RedBlackTree):
    '''An augmented red-black tree for storing intervals 
       (generally of time, rather than pitch).
    '''

    __slots__ = ('_intervals', '_root', '_sentinel')

    def __init__(self, intervals = [ ]):
        self._sentinel = _IntervalNode(0)
        self._sentinel.red = True
        self._sentinel.left = self._sentinel
        self._sentinel.right = self._sentinel
        self._sentinel.parent = self._sentinel
        self._root = self._sentinel
        self._intervals = [ ]
        self.insert(intervals)

    ## OVERLOADS ##

    def __contains__(self, item):
        if item in self._intervals:
            return True
        else:
            return False

    def __iter__(self):
        for interval in self.inorder:
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

    ## PRIVATE ATTRIBUTES ##

    ## PUBLIC ATTRIBUTES ##

    @property
    def high_max(self):
        if self:
            return self._root.high_max
        else:
            return None

    @property
    def high_min(self):
        if self:
            return self._root.high_min
        else:
            return None

    @property
    def inorder(self):
        if self:
            intervals = [ ]
            nodes = tuple(self._sort_nodes_inorder( ))
            for node in nodes:
                intervals.extend(sorted(node.payload, key=lambda x: x.signature))
            return tuple(intervals)
        else:
            return ( )

    @property
    def intervals(self):
        return tuple(self._intervals)

    @property
    def low_max(self):
        if self:
            return self._find_maximum(self._root).key
            #return self._root._maximum.key
        else:
            return None

    @property
    def low_min(self):
        if self:
            return self._find_minimum(self._root).key
            #return self._root._minimum.key
        else:
            return None

    ## PRIVATE METHODS ##

    def _update_high_extrema(self):   
        def recurse(node):
            max = min = node.payload[0].high
            for interval in node.payload[1:]:
                if max < interval.high:
                    max = interval.high
                if interval.high < min:
                    min = interval.high
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
            node.high_max = max
            node.high_min = min
            return max, min
        if self._root != self._sentinel:
            recurse(self._root)
    
## PUBLIC METHODS ##

    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if node != self._sentinel and node.key <= high and low <= node.high_max:
                for interval in node.payload:
                    if interval.low <= high and low <= interval.high:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and self._find_minimum(node.left).key <= high \
                and low <= node.left.high_max:
                intervals.extend(recurse(node.left, low, high))
            if node.right != self._sentinel \
                and self._find_minimum(node.right).key <= high \
                and low <= node.right.high_max:
                intervals.extend(recurse(node.right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], BoundedInterval)
            low, high = args[0].low, args[0].high
        elif len(args) == 2:
            low, high = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (low, high)])
            assert low <= high
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, low, high), key=lambda x: x.signature))

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node.key <= offset and offset <= node.high_max:
                for interval in node.payload:
                    if interval.low <= offset and offset <= interval.high:
                        intervals.append(interval)
            if node.left != self._sentinel and self._find_minimum(node.left).key <= offset \
                and offset <= node.left.high_max:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and self._find_minimum(node.right).key <= offset \
                and offset <= node.right.high_max:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_after_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
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
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node.key and node.high_min <= high:
                for interval in node.payload:
                    if low <= interval.low and interval.high <= high:
                        intervals.append(interval)
            if node.left != self._sentinel \
                and low <= self._find_maximum(node.left).key \
                and node.left.high_min <= high:
                intervals.extend(recurse(node.left, low, high))
            if node.right != self._sentinel \
                and low <= self._find_maximum(node.right).key \
                and node.right.high_min <= high:
                intervals.extend(recurse(node.right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], BoundedInterval)
            low, high = args[0].low, args[0].high
        elif len(args) == 2:
            low, high = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (low, high)])
            assert low <= high
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, low, high), key=lambda x: x.signature))
       
    def find_intervals_starting_at_offset(self, offset):
        assert isinstance(offset, (int, Fraction))
        node = self._find_by_key(offset)
        if node is not None and node != self._sentinel:
            return tuple(sorted(node.payload, key=lambda x: x.signature))
        else:
            return ( )

    def find_intervals_starting_before_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
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
            intervals = [ ]
            if node.key <= offset and offset <= node.high_max:
                for interval in node.payload:
                    if interval.low == offset or interval.high == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and offset <= node.left.high_max:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and self._find_minimum(node.right).key <= offset \
                and offset <= node.right.high_max:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_within_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node.key <= high:
                intervals.extend(node.payload)
            if node.left != self._sentinel and \
                low <= self._find_maximum(node.left).key and \
                self._find_minimum(node.left).key <= high:
                intervals.extend(recurse(node.left, low, high))
            if node.right != self._sentinel and \
                low <= self._find_maximum(node.right).key and \
                self._find_minimum(node.right).key <= high:
                intervals.extend(recurse(node.right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], BoundedInterval)
            low, high = args[0].low, args[0].high
        elif len(args) == 2:
            low, high = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (low, high)])
            assert low <= high
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, low, high), key=lambda x: x.signature))

    def find_intervals_stopping_after_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if offset < node.high_max:
                for interval in node.payload:
                    if offset < interval.high:
                        intervals.append(interval)
            if node.left != self._sentinel and offset < node.left.high_max:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and offset < node.right.high_max:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_at_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node.high_min <= offset and offset <= node.high_max:
                for interval in node.payload:
                    if interval.high == offset:
                        intervals.append(interval)
            if node.left != self._sentinel and offset <= node.left.high_max:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and node.right.high_min <= offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_before_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node.key <= offset and node.high_min < offset:
                for interval in node.payload:
                    if interval.high < offset:
                        intervals.append(interval)
            if node.left != self._sentinel and node.left.high_min < offset:
                intervals.extend(recurse(node.left, offset))
            if node.right != self._sentinel and node.right.high_min < offset:
                intervals.extend(recurse(node.right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_within_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node.high_max and node.high_min <= high:
                for interval in node.payload:
                    if low <= interval.high <= high:
                        intervals.append(interval)
            if node.left != self._sentinel and \
                low <= node.left.high_max and \
                node.left.high_min <= high:
                intervals.extend(recurse(node.left, low, high))
            if node.right != self._sentinel and \
                low <= node.right.high_max and \
                node.right.high_min <= high:
                intervals.extend(recurse(node.right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], BoundedInterval)
            low, high = args[0].low, args[0].high
        elif len(args) == 2:
            low, high = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (low, high)])
            assert low <= high
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, low, high), key=lambda x: x.signature))

    def insert(self, args):
        if isinstance(args, BoundedInterval):
            intervals = [args]
        elif isinstance(args, (list, tuple)):
            assert all([isinstance(i, BoundedInterval) for i in args])
            intervals = args
        else:
            raise ValueError
        for interval in intervals:
            #interval_copy = interval.__class__(interval)
            node = self._find_by_key(interval.low)
            if node is not None:
                node.payload.append(interval)
                #node.payload.append(interval_copy)
            else:
                node = _IntervalNode(interval.low, interval)
                node.left = self._sentinel
                node.right = self._sentinel
                node.parent = self._sentinel
                #node = _IntervalNode(interval.low, interval_copy)
                self._insert_node(node)
            self._intervals.append(interval)
            #self._intervals.append(interval_copy)
        self._update_high_extrema( )

    def remove(self, args):
        if isinstance(args, BoundedInterval):
            intervals = [args]
        elif isinstance(args, (list, tuple)):
            assert all([isinstance(i, BoundedInterval) for i in args])
            intervals = args
        else:
            raise ValueError
        assert all([interval in self for interval in intervals])
        for interval in intervals:
            node = self._find_by_key(interval.low)
            node.payload.pop(node.payload.index(interval))
            if not node.payload:
                self._delete_node(node)
            self._intervals.pop(self._intervals.index(interval))
        self._update_high_extrema( )

    def scale_member_interval_by_value(self, interval, value):
        assert interval in self._intervals
        new_interval = interval.scale_by_value(value)
        if new_interval != interval:
            self.remove(interval)
            self.insert(new_interval)
            return new_interval
        else:
            return interval

    def scale_member_interval_to_value(self, interval, value):
        assert interval in self._intervals
        new_interval = interval.scale_to_value(value)
        if new_interval != interval:
            self.remove(interval)
            self.insert(new_interval)
            return new_interval
        else:
            return interval

    def shift_member_interval_by_value(self, interval, value):
        assert interval in self._intervals
        new_interval = interval.shift_by_value(value)
        if new_interval != interval:
            self.remove(interval)
            self.insert(new_interval)
            return new_interval
        else:
            return interval        

    def shift_member_interval_to_value(self, interval, value):
        assert interval in self._intervals
        new_interval = interval.shift_to_value(value)
        if new_interval != interval:
            self.remove(interval)
            self.insert(new_interval)
            return new_interval
        else:
            return interval

    def split_member_interval_at_value(self, interval, value):
        assert interval in self._intervals
        splits = interval.split_at_value(value)
        if splits != interval:
            self.remove(interval)
            self.insert(splits)
            return splits
        else:
            return interval
