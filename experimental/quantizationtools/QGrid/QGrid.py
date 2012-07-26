from abjad.tools import abctools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridContainer import QGridContainer
from experimental.quantizationtools.QGridLeaf import QGridLeaf
from experimental.quantizationtools.ProxyQEvent import ProxyQEvent
import copy


class QGrid(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_leaves', '_next_downbeat', '_offsets', '_root_node')

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
        self._leaves = self._root_node.leaves + (self._next_downbeat,)
        self._offsets = tuple([x.offset for x in self.leaves[:-1]] + [durationtools.Offset(1)])

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
        return self._leaves

    @property
    def next_downbeat(self):
        return self._next_downbeat

    @property
    def offsets(self):
        return self._offsets

    @property
    def root_node(self):
        return self._root_node
