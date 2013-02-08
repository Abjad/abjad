import abc
import fractions
import inspect
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.datastructuretools.TreeNode import TreeNode


class RhythmTreeNode(TreeNode):
    '''Abstract base class of nodes in a rhythm tree structure.'''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, duration=1, name=None):
        TreeNode.__init__(self, name=name)
        self._duration = 0
        self._offset = durationtools.Offset(0)
        self._offsets_are_current = False
        self.duration = duration

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, pulse_duration):
        raise NotImplemented

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
                    current_offset += child.prolated_duration
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _pretty_rtm_format_pieces(self):
        raise NotImplemented

    @property
    def _state_flag_names(self):
        return ('_offsets_are_current',)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def graphviz_format(self):
        return self.graphviz_graph.graphviz_format

    @abc.abstractproperty
    def graphviz_graph(self):
        raise NotImplemented

    @property
    def parentage_ratios(self):
        '''A sequence describing the relative durations of the nodes in a
        node's improper parentage.

        The first item in the sequence is the duration of the root node, and
        subsequent items are pairs of the duration of the next node in the
        parentage chain and the total duration of that node and its siblings:


        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(duration=1)
            >>> b = rhythmtreetools.RhythmTreeContainer(duration=2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(duration=3)
            >>> d = rhythmtreetools.RhythmTreeLeaf(duration=4)
            >>> e = rhythmtreetools.RhythmTreeLeaf(duration=5)

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

        Return tuple.
        '''
        result = []
        node = self
        while node.parent is not None:
            result.append((node.duration, node.parent.contents_duration))
            node = node.parent
        result.append(node.duration)
        return tuple(reversed(result))

    @property
    def pretty_rtm_format(self):
        '''The node's pretty-printed RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> print tree.pretty_rtm_format
            (1 (
                (1 (
                    1
                    1))
                (1 (
                    1
                    1))))

        Return string.
        '''
        return '\n'.join(self._pretty_rtm_format_pieces)

    @property
    def prolated_duration(self):
        '''The prolated duration of the node:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree.prolated_duration
            Duration(1, 1)

        ::

            >>> tree[1].prolated_duration
            Duration(1, 2)

        ::

            >>> tree[1][1].prolated_duration
            Duration(1, 4)

        Return `Duration` instance.
        '''
        return self.prolation * self.duration

    @property
    def prolation(self):
        return mathtools.cumulative_products(self.prolations)[-1]

    @property
    def prolations(self):
        prolations = [durationtools.Multiplier(1)]
        improper_parentage = self.improper_parentage
        for child, parent in sequencetools.iterate_sequence_pairwise_strict(improper_parentage):
            prolations.append(durationtools.Multiplier(parent.duration, parent.contents_duration))
        return tuple(prolations)

    @abc.abstractproperty
    def rtm_format(self):
        '''The node's RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> tree.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

        Return string.
        '''
        raise NotImplemented

    @property
    def start_offset(self):
        '''The starting offset of a node in a rhythm-tree relative the root:

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

        Return Offset instance.
        '''
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def stop_offset(self):
        '''The stopping offset of a node in a rhythm-tree relative the root.
        '''
        return self.start_offset + self.prolated_duration

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def duration():
        def fget(self):
            '''The node's duration in pulses:

            ::

                >>> node = rhythmtreetools.RhythmTreeLeaf(duration=1)
                >>> node.duration
                Duration(1, 1)

            ::

                >>> node.duration = 2
                >>> node.duration
                Duration(2, 1)

            Return int.
            '''
            return self._duration
        def fset(self, arg):
            if not isinstance(arg, fractions.Fraction):
                arg = durationtools.Duration(arg)
            assert 0 < arg
            self._duration = arg
            self._mark_entire_tree_for_later_update()
        return property(**locals())

