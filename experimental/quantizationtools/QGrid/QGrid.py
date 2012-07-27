from abjad.tools import abctools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridContainer import QGridContainer
from experimental.quantizationtools.QGridLeaf import QGridLeaf
from experimental.quantizationtools.ProxyQEvent import ProxyQEvent
import copy


class QGrid(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_next_downbeat', '_root_node')

    ### INITIALIZATION ###

    def __init__(self, root_node=None, next_downbeat=None):
        if root_node is None:
            root_node = QGridContainer(1, [QGridLeaf(1)])
        assert isinstance(root_node, QGridContainer)

        if next_downbeat is None:
            next_downbeat = QGridLeaf(1)
        assert isinstance(next_downbeat, QGridLeaf)

        self._root_node = root_node
        self._next_downbeat = next_downbeat

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return self.__deepcopy__(None)

    def __deepcopy__(self, memo):
        root_node, next_downbeat = self.__getnewargs__()
        return type(self)(copy.copy(root_node), copy.copy(next_downbeat))

    def __eq__(self, other):
        if type(self) == type(other):
            if self.root_node == other.root_node:
                if self.next_downbeat == other.next_downbeat:
                    return True
        return False

    def __getnewargs__(self):
        return (self.root_node, self.next_downbeat)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        '''All of the leaf nodes in the QGrid, includeing the next downbeat's node.'''
        return self._root_node.leaves + (self._next_downbeat,)

    @property
    def next_downbeat(self):
        '''The node representing the "next" downbeat after the contents
        of the QGrid's tree.
        '''
        return self._next_downbeat

    @property
    def offsets(self):
        '''The offsets between 0 and 1 of all of the leaf nodes in the QGrid.'''
        return tuple([x.offset for x in self.leaves[:-1]] + [durationtools.Offset(1)])

    @property
    def root_node(self):
        return self._root_node

    ### PUBLIC METHODS ###

    def subdivide_leaf(self, leaf, subdivisions):
        index = leaf.parent.index(leaf)
        container = QGridContainer(
            leaf.duration, [
                QGridLeaf(subdivision) for subdivision in subdivisions
            ])
        leaf.parent[index] = container
        return leaf.q_events

    def subdivide_leaves(self, pairs):
        pairs = sorted(dict(pairs).items())
        leaf_indices = [pair[0] for pair in pairs]
        subdivisions = [pair[1] for pair in pairs]

        all_leaves = self.leaves
        leaves_to_subdivide = [all_leaves[idx] for idx in leaf_indices]

        q_events = []
        for i, leaf in enumerate(leaves_to_subdivide):

            next_leaf = all_leaves[all_leaves.index(leaf) + 1]
            if next_leaf is self.next_downbeat:
                next_leaf_offset = durationtools.Offset(1)
            else:
                next_leaf_offset = next_leaf.offset
            
            q_events.extend(self.subdivide_leaf(leaf, subdivisions[i]))
            for q_event in tuple(next_leaf.q_events):
                if q_event.offset < next_leaf_offset:
                    q_events.append(next_leaf.q_events.pop(next_leaf.q_events.index(q_event)))

        return q_events
