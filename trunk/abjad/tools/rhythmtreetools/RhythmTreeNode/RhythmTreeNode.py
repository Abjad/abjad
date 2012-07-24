from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import durationtools
from fractions import Fraction


class RhythmTreeNode(abctools.AbjadObject):
    '''Abstract base class of nodes in a rhythm tree structure.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_offset', '_offsets_are_current', '_parent')

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, duration):
        self._offset = durationtools.Offset(0)
        self._offsets_are_current = False
        self._parent = None
        self.duration = duration

    ### SPECIAL METHODS ###

    @abstractmethod
    def __call__(self, pulse_duration):
        raise NotImplemented

    ### PRIVATE METHODS ###

    def _get_node_state_flags(self):
        state_flags = {}
        for name in self._state_flag_names:
            state_flags[name] = True
            for node in self.improper_parentage:
                if not getattr(node, name):
                    state_flags[name] = False
                    break
        return state_flags

    def _mark_entire_tree_for_later_update(self):
        for node in self.improper_parentage:
            for name in self._state_flag_names:
                setattr(node, name, False)

    def _switch_parent(self, new_parent):
        if self._parent is not None:
            index = self._parent.index(self)
            self._parent._children.pop(index)
        self._parent = new_parent

    def _update_offsets_of_entire_tree(self):
        def recurse(container, current_offset):
            container._offset = current_offset
            container._offsets_are_current = True
            for child in container:
                if hasattr(child, 'children'):
                    current_offset = recurse(child, current_offset)
                else:
                    child._offset = current_offset
                    child._offsets_are_current = True
                    current_offset += child.prolated_duration
            return current_offset
        offset = durationtools.Offset(0)
        root = self.root_node
        if root is self:
            self._offset = offset
            self._offsets_are_current = True
        else:
            recurse(root, offset)

    def _update_offsets_of_entire_tree_if_necessary(self):
        if not self._get_node_state_flags()['_offsets_are_current']:
            self._update_offsets_of_entire_tree()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _state_flag_names(self):
        return ('_offsets_are_current',)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def improper_parentage(self):
        node = self
        parentage = [node]
        while node.parent is not None:
            node = node.parent
            parentage.append(node)
        return tuple(parentage)

    @property
    def offset(self):
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def parent(self):
        '''The node's parent node.'''
        return self._parent

    @property
    def prolated_duration(self):
        '''The prolated duration of the node.'''
        prolation = durationtools.Duration(1)
        node = self
        while node.parent is not None:
            duration = node.duration
            total_duration = node.parent.contents_duration
            prolation *= Fraction(duration, total_duration)
            node = node.parent
        prolation *= node.duration
        return prolation

    @property
    def proper_parentage(self):
        return self.improper_parentage[1:]

    @property
    def root_node(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    @abstractproperty
    def rtm_format(self):
        '''The node's RTM format.'''
        raise NotImplemented

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def duration():
        def fget(self):
            '''The node's duration in pulses.'''
            return self._duration
        def fset(self, arg):
            assert isinstance(arg, int)
            assert 0 < arg
            self._duration = arg
        return property(**locals())

