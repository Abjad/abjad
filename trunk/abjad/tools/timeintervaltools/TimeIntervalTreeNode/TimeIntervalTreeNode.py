# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeIntervalTreeNode(AbjadObject):
    r'''A red-black node in an TimeIntervalTree.

    Duplicate payloads are supported by maintaining a list of TimeIntervals.

    Not composer-safe.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_earliest_stop',
        '_key',
        '_latest_stop',
        '_left',
        '_parent',
        '_payload',
        '_red',
        '_right',
        )

    ### INITIALIZER ###

    def __init__(self, key, intervals=None):
        from abjad.tools import timeintervaltools
        self._earliest_stop = None
        self._key = durationtools.Offset(key)
        self._latest_stop = None
        self._left = None
        self._parent = None
        self._red = True
        self._right = None
        self._payload = []
        if isinstance(intervals, (list, set, tuple)):
            assert all(isinstance(interval, timeintervaltools.TimeInterval)
                for interval in intervals)
            self.payload.extend(intervals)
        elif isinstance(intervals, (timeintervaltools.TimeInterval,
            type(None))):
            self.payload.append(intervals)
        else:
            raise ValueError('Only accepts single or multiple instances of TimeInterval.')

    ### PUBLIC PROPERTIES ###

    @apply
    def earliest_stop():
        def fget(self):
            return self._earliest_stop
        def fset(self, expr):
            self._earliest_stop = durationtools.Offset(expr)
        return property(**locals())

    @property
    def grandparent(self):
        if self.parent is not None and self.parent.parent is not None:
            return self.parent.parent
        else:
            return None

    @property
    def is_left_child(self):
        if self.parent is not None and self == self.parent.left:
            return True
        else:
            return False

    @property
    def is_right_child(self):
        if self.parent is not None and self == self.parent.right:
            return True
        else:
            return False

    @property
    def key(self):
        return self._key

    @apply
    def latest_stop():
        def fget(self):
            return self._latest_stop
        def fset(self, expr):
            self._latest_stop = durationtools.Offset(expr)
        return property(**locals())

    @apply
    def left():
        def fget(self):
            return self._left
        def fset(self, expr):
            self._left = expr
        return property(**locals())

    @apply
    def parent():
        def fget(self):
            return self._parent
        def fset(self, expr):
            self._parent = expr
        return property(**locals())

    @property
    def payload(self):
        return self._payload

    @apply
    def red():
        def fget(self):
            return self._red
        def fset(self, expr):
            self._red = expr
        return property(**locals())

    @apply
    def right():
        def fget(self):
            return self._right
        def fset(self, expr):
            self._right = expr
        return property(**locals())

    @property
    def sibling(self):
        if self.parent is not None:
            if self.is_left_child:
                return self.parent.right
            else:
                return self.parent.left

    @property
    def uncle(self):
        if self.grandparent is not None:
            if self.parent.is_left_child:
                return self.grandparent.right
            else:
                return self.grandparent.left
        return None
