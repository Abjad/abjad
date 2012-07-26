from abjad.tools import abctools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridContainer import QGridContainer
from experimental.quantizationtools.QGridLeaf import QGridLeaf


class QGrid(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_leaves', '_next_downbeat', '_offsets', '_root_node')

    ### INITIALIZATION ###

    def __init__(self):
        self._root_node = QGridContainer()
        self._next_downbeat = QGridLeaf()
        self._leaves = self._root_node.leaves + (self._next_downbeat,)
        self._offsets = tuple([x.offset for x in self.leaves[:-1]] + [durationtools.Offset(1)])

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
