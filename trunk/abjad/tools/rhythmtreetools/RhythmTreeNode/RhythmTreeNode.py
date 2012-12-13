import abc
import fractions
import inspect
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class RhythmTreeNode(AbjadObject):
    '''Abstract base class of nodes in a rhythm tree structure.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_duration', '_offset', '_offsets_are_current', '_parent')

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, duration):
        self._offset = durationtools.Offset(0)
        self._offsets_are_current = False
        self._parent = None
        self.duration = duration

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, pulse_duration):
        raise NotImplemented

    def __copy__(self, *args):
        return self.__deepcopy__(None)
        
    @abc.abstractmethod
    def __deepcopy__(self, memo):
        raise NotImplemented

    @abc.abstractmethod
    def __getnewargs__(self):
        raise NotImplemented

    def __getstate__(self):
        state = {}
        for klass in inspect.getmro(self.__class__):
            if hasattr(klass, '__slots__'):
                for slot in klass.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

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
        self._mark_entire_tree_for_later_update()

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
    def depth(self):
        '''The depth of a node in a rhythm-tree structure:

        ::

            >>> rtm = '(4 ((2 (1 1)) (2 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
        
        ::

            >>> tree.depth
            0

        ::

            >>> tree[0].depth
            1

        ::

            >>> tree[0][0].depth
            2

        Return int.
        '''
        node = self
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth

    @property
    def depthwise_inventory(self):
        '''A dictionary of all nodes in a rhythm-tree, organized by their
        depth relative the root node:

        ::

            >>> rtm = '(4 ((2 (1 1)) (2 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> inventory = tree.depthwise_inventory
            >>> for depth in sorted(inventory):
            ...     print 'DEPTH: {}'.format(depth)
            ...     for node in inventory[depth]:
            ...         print str(node.duration), str(node.start_offset)
            ...
            DEPTH: 0
            4 0
            DEPTH: 1
            2 0
            2 2
            DEPTH: 2
            1 0
            1 1
            1 2
            1 3

        Return dictionary.
        '''
        inventory = {}
        def recurse(node):
            if node.depth not in inventory:
                inventory[node.depth] = []
            inventory[node.depth].append(node)
            if hasattr(node, 'children'):
                for child in node.children:
                    recurse(child)
        recurse(self)
        return inventory

    @property
    def graph_order(self):
        order = []
        for parent, child in sequencetools.iterate_sequence_pairwise_strict(
            reversed(self.improper_parentage)):
            order.append(parent.index(child))
        return tuple(order)

    @property
    def improper_parentage(self):
        '''The improper parentage of a node in a rhythm-tree, being the 
        sequence of node beginning with itself and ending with the root node
        of the tree:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.improper_parentage == (a,)
            True

        ::

            >>> b.improper_parentage == (b, a)
            True

        ::

            >>> c.improper_parentage == (c, b, a)
            True

        Return tuple of `RhythmTreeNode` instances.
        '''
        node = self
        parentage = [node]
        while node.parent is not None:
            node = node.parent
            parentage.append(node)
        return tuple(parentage)

    @property
    def parent(self):
        '''The node's parent node:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.parent is None
            True

        ::

            >>> b.parent is a
            True

        ::

            >>> c.parent is b
            True

        Return `RhythmTreeNode` instance.
        '''
        return self._parent

    @property
    def parentage_ratios(self):
        '''A sequence describing the relative durations of the nodes in a
        node's improper parentage.

        The first item in the sequence is the duration of the root node, and
        subsequent items are pairs of the duration of the next node in the
        parentage chain and the total duration of that node and its siblings:


        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeContainer(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)
            >>> d = rhythmtreetools.RhythmTreeLeaf(4)
            >>> e = rhythmtreetools.RhythmTreeLeaf(5)

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

    @property
    def proper_parentage(self):
        '''The proper parentage of a node in a rhythm-tree, being the 
        sequence of node beginning with the node's immediate parent and
        ending with the root node of the tree:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.proper_parentage == ()
            True

        ::

            >>> b.proper_parentage == (a,)
            True

        ::

            >>> c.proper_parentage == (b, a)
            True

        Return tuple of `RhythmTreeNode` instances.
        '''
        return self.improper_parentage[1:]

    @property
    def root_node(self):
        '''The root node of the rhythm-tree: that node in the tree which has
        no parent:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.root_node is a
            True
            >>> b.root_node is a
            True
            >>> c.root_node is a
            True

        Return `RhythmTreeNode` instance.
        '''
        node = self
        while node.parent is not None:
            node = node.parent
        return node

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

                >>> node = rhythmtreetools.RhythmTreeLeaf(1)
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

