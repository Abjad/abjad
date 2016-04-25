# -*- coding: utf-8 -*-
import abc
import fractions
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


class RhythmTreeMixin(abctools.AbjadObject):
    r'''Rhythm-tree node abstract base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, preprolated_duration=1):
        self._duration = 0
        self._offset = durationtools.Offset(0)
        self._offsets_are_current = False
        self.preprolated_duration = preprolated_duration

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, pulse_duration):
        r'''Calls rhythm tree node on `pulse_duration`.
        '''
        raise NotImplementedError

    ### PRIVATE METHODS ###

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
                    current_offset += child.duration
            return current_offset
        offset = durationtools.Offset(0)
        root = self.root
        if root is self and not hasattr(self, 'children'):
            self._offset = offset
            self._offsets_are_current = True
        else:
            recurse(root, offset)

    def _update_offsets_of_entire_tree_if_necessary(self):
        if not self._get_node_state_flags()['_offsets_are_current']:
            self._update_offsets_of_entire_tree()

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _pretty_rtm_format_pieces(self):
        raise NotImplementedError

    @property
    def _state_flag_names(self):
        return ('_offsets_are_current',)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''The preprolated_duration of the node:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree.duration
            Duration(1, 1)

        ::

            >>> tree[1].duration
            Duration(1, 2)

        ::

            >>> tree[1][1].duration
            Duration(1, 4)

        Return `Duration` instance.
        '''
        return self.prolation * self.preprolated_duration

    @property
    def parentage_ratios(self):
        r'''A sequence describing the relative durations of the nodes in a
        node's improper parentage.

        The first item in the sequence is the preprolated_duration of
        the root node, and subsequent items are pairs of the
        preprolated duration of the next node in the parentage and
        the total preprolated_duration of that node and its siblings:


        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(preprolated_duration=1)
            >>> b = rhythmtreetools.RhythmTreeContainer(preprolated_duration=2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3)
            >>> d = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=4)
            >>> e = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=5)

        ::

            >>> a.extend([b, c])
            >>> b.extend([d, e])

        ::

            >>> a.parentage_ratios
            (Duration(1, 1),)

        ::

            >>> b.parentage_ratios
            (Duration(1, 1), (Duration(2, 1), Duration(5, 1)))

        ::

            >>> c.parentage_ratios
            (Duration(1, 1), (Duration(3, 1), Duration(5, 1)))

        ::

            >>> d.parentage_ratios
            (Duration(1, 1), (Duration(2, 1), Duration(5, 1)), (Duration(4, 1), Duration(9, 1)))

        ::

            >>> e.parentage_ratios
            (Duration(1, 1), (Duration(2, 1), Duration(5, 1)), (Duration(5, 1), Duration(9, 1)))

        Returns tuple.
        '''
        result = []
        node = self
        while node.parent is not None:
            result.append(
                (node.preprolated_duration, node.parent._contents_duration))
            node = node.parent
        result.append(node.preprolated_duration)
        return tuple(reversed(result))

    @property
    def preprolated_duration(self):
        r'''The node's preprolated_duration in pulses:

        ::

            >>> node = rhythmtreetools.RhythmTreeLeaf(
            ...     preprolated_duration=1)
            >>> node.preprolated_duration
            Duration(1, 1)

        ::

            >>> node.preprolated_duration = 2
            >>> node.preprolated_duration
            Duration(2, 1)

        Returns int.
        '''
        return self._duration

    @preprolated_duration.setter
    def preprolated_duration(self, arg):
        if not isinstance(arg, fractions.Fraction):
            arg = durationtools.Duration(arg)
        assert 0 < arg
        self._duration = arg
        self._mark_entire_tree_for_later_update()

    @property
    def pretty_rtm_format(self):
        r'''The node's pretty-printed RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> print(tree.pretty_rtm_format)
            (1 (
                (1 (
                    1
                    1))
                (1 (
                    1
                    1))))

        Returns string.
        '''
        return '\n'.join(self._pretty_rtm_format_pieces)

    @property
    def prolation(self):
        r'''Prolation of rhythm tree node.

        Returns multiplier.
        '''
        return mathtools.cumulative_products(self.prolations)[-1]

    @property
    def prolations(self):
        r'''Prolations of rhythm tree node.

        Returns tuple.
        '''
        prolations = [durationtools.Multiplier(1)]
        improper_parentage = self.improper_parentage
        for child, parent in \
            sequencetools.iterate_sequence_nwise(improper_parentage):
            prolations.append(durationtools.Multiplier(
                parent.preprolated_duration, parent._contents_duration))
        return tuple(prolations)

    @abc.abstractproperty
    def rtm_format(self):
        r'''The node's RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> tree.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

        Returns string.
        '''
        raise NotImplementedError

    @property
    def start_offset(self):
        r'''The starting offset of a node in a rhythm-tree relative the root.

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree.start_offset
            Offset(0, 1)

        ::

            >>> tree[1].start_offset
            Offset(1, 2)

        ::

            >>> tree[0][1].start_offset
            Offset(1, 4)

        Returns Offset instance.
        '''
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def stop_offset(self):
        r'''The stopping offset of a node in a rhythm-tree relative the root.
        '''
        return self.start_offset + self.duration
