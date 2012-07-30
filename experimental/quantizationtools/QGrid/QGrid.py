from abjad.tools import abctools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridContainer import QGridContainer
from experimental.quantizationtools.QGridLeaf import QGridLeaf
from experimental.quantizationtools.QEventProxy import QEventProxy
import bisect
import copy


class QGrid(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_next_downbeat', '_root_node')

    ### INITIALIZATION ###

    def __init__(self, root_node=None, next_downbeat=None):
        if root_node is None:
            root_node = QGridLeaf(1)
        assert isinstance(root_node, (QGridLeaf, QGridContainer))

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
        if isinstance(self._root_node, QGridLeaf):
            return (self._root_node, self._next_downbeat)
        return self._root_node.leaves + (self._next_downbeat,)

    @property
    def next_downbeat(self):
        '''The node representing the "next" downbeat after the contents
        of the QGrid's tree.
        '''
        return self._next_downbeat

    @property
    def distance(self):
        q_event_count = 0
        absolute_distance = 0
        for leaf, offset in zip(self.leaves, self.offsets):
            for q_event in leaf.q_events:
                absolute_distance += abs(q_event.offset - offset)
                q_event_count += 1
        if q_event_count:
            return absolute_distance / q_event_count
        return None

    @property
    def offsets(self):
        '''The offsets between 0 and 1 of all of the leaf nodes in the QGrid.'''
        return tuple([x.offset for x in self.leaves[:-1]] + [durationtools.Offset(1)])

    @property
    def root_node(self):
        return self._root_node

    ### PUBLIC METHODS ###

    def fit_q_events(self, q_events):
        assert all([isinstance(x, QEventProxy) for x in q_events])
        leaves, offsets = self.leaves, self.offsets
        for q_event in q_events:
            idx = bisect.bisect_left(offsets, q_event.offset)
            if q_event.offset == offsets[idx]:
                leaves[idx].q_events.append(q_event)
            else:
                left, right = offsets[idx - 1], offsets[idx]
                left_diff = abs(left - q_event.offset)
                right_diff = abs(right - q_event.offset)
                if right_diff < left_diff:
                    leaves[idx].q_events.append(q_event)
                else:
                    leaves[idx - 1].q_events.append(q_event)

    def sort_q_events_by_index(self):
        for leaf in self.leaves:
            leaf.q_events.sort(key=lambda x: x.index)

    def subdivide_leaf(self, leaf, subdivisions):
        container = QGridContainer(
            leaf.duration, [
                QGridLeaf(subdivision) for subdivision in subdivisions
            ])
        if leaf.parent is not None:
            index = leaf.parent.index(leaf)
            leaf.parent[index] = container
        else: # otherwise, our root node is just a QGridLeaf
            self._root_node = container
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
