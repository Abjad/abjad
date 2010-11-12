from fractions import Fraction
from abjad.tools.treetools._Interval import _Interval
from abjad.tools.treetools._IntervalTreeNode import _IntervalTreeNode


class IntervalTree(object):
    '''An augmented red-black tree for storing intervals 
       (generally of time, rather than pitch).
    '''

    __slots__ = ('_intervals', '_root', )

    def __init__(self, intervals = [ ]):
        self._intervals = [ ]
        self._root = None
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
        if self._root is not None:
            return len(self._root)
        else:
            return 0

    def __str__(self):
        if self._root is None: return '<empty tree>'
        def recurse(node):  
            if node is None: return [], 0, 0
            if node._red:
                color = 'r'
            else:
                color = 'b'
            label = '%s%s' % (node._key, color)
            left_lines, left_pos, left_width = recurse(node._left)
            right_lines, right_pos, right_width = recurse(node._right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node._parent is not None and \
               node is node._parent._left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self._root) [0])

    ## PRIVATE ATTRIBUTES ##

    ## PUBLIC ATTRIBUTES ##

    @property
    def high_max(self):
        if self:
            return self._root._high_max
        else:
            return None

    @property
    def high_min(self):
        if self:
            return self._root._high_min
        else:
            return None

    @property
    def inorder(self):
        if self:
            return tuple(self._root._inorder)
        else:
            return ( )

    @property
    def intervals(self):
        return tuple(self._intervals)

    @property
    def low_max(self):
        if self:
            return self._root._maximum._key
        else:
            return None

    @property
    def low_min(self):
        if self:
            return self._root._minimum._key
        else:
            return None

    ## PRIVATE METHODS ##

    def _find_node_by_key(self, key):
        def recurse(node, key):
            if node is None or node._key == key:
                return node
            if key < node._key:
                return recurse(node._left, key)
            else:
                return recurse(node._right, key)        
        return recurse(self._root, key)

    def _insert_node(self, z):
        '''Binary search tree insertion; from CLRS.'''
        y = None
        x = self._root

        while x is not None:
            y = x
            if z._key < x._key:
                x = x._left
            else:
                x = x._right
        z._parent = y

        if y is None:
            self._root = z
        elif z._key < y._key:
            y._left = z
        else:
            y._right = z

        z._left = None
        z._right = None
        z._red = True
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        '''Rebalance red-black tree; from CLRS.'''
        while z != self._root and z._parent._red:
            y = z._uncle
            if y is not None and y._red:
                z._parent._red = False
                y._red = False
                z._grandparent._red = True
                z = z._grandparent

            elif z._parent._is_left_child:
                if z._is_right_child:
                    z = z._parent
                    self._rotate_left(z)
                z._parent._red = False
                if z._grandparent is not None:
                    z._grandparent._red = True
                    self._rotate_right(z._grandparent)
                else:
                    break

            elif z._parent._is_right_child:
                if z._is_left_child:
                    z = z._parent
                    self._rotate_right(z)
                z._parent._red = False
                if z._grandparent is not None:
                    z._grandparent._red = True
                    self._rotate_left(z._grandparent)
                else:
                    break

        self._root._red = False

    def _delete_node(self, z):
        '''Binary search tree node deletion; from CLRS.'''
        if z._left is None or z._right is None:
            y = z
        else:
            y = z._successor

        if y._left is not None:
            x = y._left
        else:
            x = y._right

        if x is not None:
            x._parent = y._parent

        if y._parent is None:
            self._root = x
        elif y._is_left_child:
            y._parent._left = x
        else:
            y._parent._right = x

        if y != z:
            z._key = y._key
            z._intervals = y._intervals
        
        if not y._red:
            self._delete_fixup(x)
        
    def _delete_fixup(self, x):
        '''Rebalance red-black tree after deletion; from CLRS.'''
        if x is None:
            return

        while x != self._root and not x._red:
            w = x._sibling
            if x._is_left_child:
                if w._red:
                    w._red = False
                    x._parent._red = True
                    self._rotate_left(x._parent)
                    w = x._parent._right
                if not w._left._red and not w._right._red:
                    w._red = True
                    x = x._parent
                else:
                    if not w._right._red:
                        w._left._red = False
                        w._red = True
                        self._rotate_right(w)
                        w = x._parent._right
                    w._red = x._parent._red
                    x._parent._red = False
                    w._right._red = False
                    self._rotate_left(x._parent)
                    x = self._root

            else:
                if w._red:
                    w._red = False
                    x._parent._red = True
                    self._rotate_right(x._parent)
                    w = x._parent._left
                if not w._right._red and not w._left._red:
                    w._red = True
                    x = x._parent
                else:
                    if not w._left._red:
                        w._right._red = False
                        w._red = True
                        self._rotate_left(w)
                        w = x._parent._left
                    w._red = x._parent._red
                    x._parent._red = False
                    w._left._red = False
                    self._rotate_right(x._parent)
                    x = self._root                

        x._red = False

    def _rotate_left(self, x):
        y = x._right
        x._right = y._left
        if y._left is not None:
            y._left._parent = x
        y._parent = x._parent
        if x._parent is None:
            self._root = y
        elif x._is_left_child:
            x._parent._left = y
        else:
            x._parent._right = y
        y._left = x
        x._parent = y
        
    def _rotate_right(self, x):
        y = x._left
        x._left = y._right
        if y._right is not None:
            y._right._parent = x
        y._parent = x._parent
        if x._parent is None:
            self._root = y
        elif x._is_left_child:
            x._parent._left = y
        else:
            x._parent._right = y
        y._right = x
        x._parent = y

    def _update_high_extrema(self):
        if self._root:
            self._root._update_high_extrema( )

    ## PUBLIC METHODS ##

    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if node._key <= high and low <= node._high_max:
                for interval in node._intervals:
                    if interval.low <= high and low <= interval.high:
                        intervals.append(interval)
            if node._left is not None \
                and node._left._minimum._key <= high \
                and low <= node._left._high_max:
                intervals.extend(recurse(node._left, low, high))
            if node._right is not None \
                and node._right._minimum._key <= high \
                and low <= node._right._high_max:
                intervals.extend(recurse(node._right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], _Interval)
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
            if node._key <= offset and offset <= node._high_max:
                for interval in node._intervals:
                    if interval.low <= offset and offset <= interval.high:
                        intervals.append(interval)
            if node._left is not None and node._left._minimum._key <= offset \
                and offset <= node._left._high_max:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and node._right._minimum._key <= offset \
                and offset <= node._right._high_max:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_after_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if offset < node._key:
                intervals.extend(node._intervals)
            if node._left is not None and offset < node._left._maximum._key:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node._key and node._high_min <= high:
                for interval in node._intervals:
                    if low <= interval.low and interval.high <= high:
                        intervals.append(interval)
            if node._left is not None \
                and low <= node._left._maximum._key \
                and node._left._high_min <= high:
                intervals.extend(recurse(node._left, low, high))
            if node._right is not None \
                and low <= node._right._maximum._key \
                and node._right._high_min <= high:
                intervals.extend(recurse(node._right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], _Interval)
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
        node = self._find_node_by_key(offset)
        if node is not None:
            return tuple(sorted(node._intervals, key=lambda x: x.signature))
        else:
            return ( )

    def find_intervals_starting_before_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node._key < offset:
                intervals.extend(node._intervals)
            if node._left is not None:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and node._right._minimum._key < offset:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node._key <= offset and offset <= node._high_max:
                for interval in node._intervals:
                    if interval.low == offset or interval.high == offset:
                        intervals.append(interval)
            if node._left is not None and offset <= node._left._high_max:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and node._right._minimum._key <= offset \
                and offset <= node._right._high_max:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_starting_within_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node._key <= high:
                intervals.extend(node._intervals)
            if node._left is not None and \
                low <= node._left._maximum._key and \
                node._left._minimum._key <= high:
                intervals.extend(recurse(node._left, low, high))
            if node._right is not None and \
                low <= node._right._maximum._key and \
                node._right._minimum._key <= high:
                intervals.extend(recurse(node._right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], _Interval)
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
            if offset < node._high_max:
                for interval in node._intervals:
                    if offset < interval.high:
                        intervals.append(interval)
            if node._left is not None and offset < node._left._high_max:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and offset < node._right._high_max:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_at_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node._high_min <= offset and offset <= node._high_max:
                for interval in node._intervals:
                    if interval.high == offset:
                        intervals.append(interval)
            if node._left is not None and offset <= node._left._high_max:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and node._right._high_min <= offset:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_before_offset(self, offset):
        def recurse(node, offset):
            intervals = [ ]
            if node._key <= offset and node._high_min < offset:
                for interval in node._intervals:
                    if interval.high < offset:
                        intervals.append(interval)
            if node._left is not None and node._left._high_min < offset:
                intervals.extend(recurse(node._left, offset))
            if node._right is not None and node._right._high_min < offset:
                intervals.extend(recurse(node._right, offset))
            return intervals
        assert isinstance(offset, (int, Fraction))
        return tuple(sorted(recurse(self._root, offset), key=lambda x: x.signature))

    def find_intervals_stopping_within_interval(self, *args):
        def recurse(node, low, high):
            intervals = [ ]
            if low <= node._high_max and node._high_min <= high:
                for interval in node._intervals:
                    if low <= interval.high <= high:
                        intervals.append(interval)
            if node._left is not None and \
                low <= node._left._high_max and \
                node._left._high_min <= high:
                intervals.extend(recurse(node._left, low, high))
            if node._right is not None and \
                low <= node._right._high_max and \
                node._right._high_min <= high:
                intervals.extend(recurse(node._right, low, high))
            return intervals
        if len(args) == 1:
            assert isinstance(args[0], _Interval)
            low, high = args[0].low, args[0].high
        elif len(args) == 2:
            low, high = args[0], args[1]
            assert all([isinstance(x, (int, Fraction)) for x in (low, high)])
            assert low <= high
        else:
            raise ValueError
        return tuple(sorted(recurse(self._root, low, high), key=lambda x: x.signature))

    def insert(self, args):
        if isinstance(args, _Interval):
            intervals = [args]
        elif isinstance(args, (list, tuple)):
            assert all([isinstance(i, _Interval) for i in args])
            intervals = args
        else:
            raise ValueError
        for interval in intervals:
            #interval_copy = interval.__class__(interval)
            node = self._find_node_by_key(interval.low)
            if node is not None:
                node._intervals.append(interval)
                #node._intervals.append(interval_copy)
            else:
                node = _IntervalTreeNode(interval.low, interval)
                #node = _IntervalTreeNode(interval.low, interval_copy)
                self._insert_node(node)
            self._intervals.append(interval)
            #self._intervals.append(interval_copy)
        self._update_high_extrema( )

    def remove(self, args):
        if isinstance(args, _Interval):
            intervals = [args]
        elif isinstance(args, (list, tuple)):
            assert all([isinstance(i, _Interval) for i in args])
            intervals = args
        else:
            raise ValueError
        assert all([interval in self for interval in intervals])
        for interval in intervals:
            node = self._find_node_by_key(interval.low)
            node._intervals.pop(node._intervals.index(interval))
            if not node._intervals:
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
