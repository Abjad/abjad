from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


class _IntervalTreeNode(object):
    '''A red-black node in an IntervalTree.
       Duplicate payloads are supported by maintaining a list of _BoundedIntervals
    '''
    
    __slots__ = ('_high_max', '_high_min', '_intervals', '_key', 
                 '_left', '_parent', '_red', '_right', )

    def __init__(self, key, intervals = None):
        assert isinstance(key, (int, Fraction))
        self._key = key

        # init intervals: a list of _BoundedInterval objects
        if isinstance(intervals, _BoundedInterval):
            self._intervals = [intervals]
        elif isinstance(intervals, (list, set, tuple)):
            assert all([isinstance(x, _BoundedInterval) for x in intervals])
            self._intervals = intervals
        else:
            self._intervals = None
        #else:
        #    raise TypeError('Node data must be a _BoundedInterval or list of _BoundedIntervals.')
        if self._intervals is not None:
            for interval in self._intervals:
                assert interval.low == self._key

        # init other tree-related properties
        self._high_max = None
        self._high_min = None
        self._left = None
        self._parent = None
        self._red = None
        self._right = None

    ## OVERLOADS ##

    def __len__(self):
        length = len(self._intervals)
        if self._left is not None:
            length += len(self._left)
        if self._right is not None:
            length += len(self._right)
        return length

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self._key, repr(self._intervals))

    ## PRIVATE ATTRIBUTES ##

    @property
    def _children(self):
        results = [ ]
        if self._left is not None:
            results.append(self._left)
        if self._right is not None:
            results.append(self._right)
        return tuple(results)

    @property
    def _grandparent(self):
        if self._parent is not None:
            if self._parent._parent is not None:
                return self._parent._parent
        return None

    @property
    def _inorder(self):
        results = [ ]
        if self._left is not None:
            results.extend(self._left._inorder)
        intervals = sorted(self._intervals, key = lambda x: x.high)
        results.extend(intervals)
        if self._right is not None:
            results.extend(self._right._inorder)
        return tuple(results)

    @property
    def _is_left_child(self):
        if self._parent is not None and self._parent._left == self:
            return True
        else:
            return False
            
    @property
    def _is_right_child(self):
        if self._parent is not None and self._parent._right == self:
            return True 
        else:
            return False

    @property
    def _maximum(self):
        node = self
        while node._right is not None:
            node = node._right
        return node

    @property
    def _minimum(self):
        node = self
        while node._left is not None:
            node = node._left
        return node

    @property
    def _predecessor(self):
        if self._left is not None:
            return self._left._maximum
        node = self
        parent = node._parent
        while parent is not None and node == parent._left:
            node = parent
            parent = node._parent
        return parent

    @property
    def _root(self):
        node = self  
        while node._parent is not None:
            node = node._parent
        return node

    @property
    def _sibling(self):
        if self._is_left_child:
            return self._parent._right
        else:
            return self._parent._left
        
    @property
    def _successor(self):
        if self._right is not None:
            return self._right._minimum
        node = self
        parent = node._parent
        while parent is not None and node == parent._right:
            node = parent
            parent = node._parent
        return parent

    @property
    def _uncle(self):
        if self._parent is not None:
            if self._parent._parent is not None:
                if self._parent._is_left_child:
                    return self._parent._parent._right
                else:
                    return self._parent._parent._left
        return None

    ## PRIVATE METHODS ##

    def _update_high_extrema(self):
        max = min = self._intervals[0].high

        for interval in self._intervals[1:]:
            if max < interval.high:
                max = interval.high
            if interval.high < min:
                min = interval.high

        if self._left is not None:
            left_max, left_min = self._left._update_high_extrema( )
            if max < left_max:
                max = left_max
            if left_min < min:
                min = left_min

        if self._right is not None:
            right_max, right_min = self._right._update_high_extrema( )
            if max < right_max:
                max = right_max
            if right_min < min:
                min = right_min

        self._high_max = max
        self._high_min = min
        return max, min
