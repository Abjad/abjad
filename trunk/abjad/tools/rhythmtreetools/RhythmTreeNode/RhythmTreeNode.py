from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from fractions import Fraction


class RhythmTreeNode(abctools.AbjadObject):
    '''Abstract base class of nodes in a rhythm tree structure.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_parent', '_duration')

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, duration):
        assert 0 < duration
        self._duration = int(duration)
        self._parent = None

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self, pulse_duration):
        raise NotImplemented

    ### PRIVATE METHODS ###

    def _switch_parent(self, new_parent):
        if self._parent is not None:
            index = self._parent.index(self)
            self._parent._children.pop(index)
        self._parent = new_parent

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def parent(self):
        '''The node's parent node.'''
        return self._parent

    @property
    def duration(self):
        '''The node's duration in pulses.'''
        return self._duration

    @property
    def prolation(self):
        '''The prolation of the node.'''
        prolation = Fraction(1)
        node = self
        while node.parent is not None:
            duration = node.duration
            total_duration = node.parent.contents_duration
            prolation *= Fraction(duration, total_duration)
            node = node.parent
        prolation *= node.duration
        return prolation

    @abstractproperty
    def rtm_format(self):
        '''The node's RTM format.'''
        raise NotImplemented
