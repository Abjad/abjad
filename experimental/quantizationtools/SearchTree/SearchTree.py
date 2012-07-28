from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from experimental.quantizationtools import QGrid


class SearchTree(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_definition',)

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self.is_valid_definition(definition)
        self._definition = self.make_definition_immutable(definition)

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
        assert isinstance(q_grid, QGrid)
        leaves = q_grid.leaves[:-1]
        indices = self.find_divisible_leaf_indices(leaves)
        subdivisions = [self.find_leaf_subdivisions(leaves[i]) for i in indices]
        combinations = [x for x in sequencetools.yield_outer_product_of_sequences(subdivisions)]
        new_q_grids = []
        for combo in combinations:
            zipped = zip(indices, combo)
            q_events = q_grid.subdivide_leaves(zipped)
        return new_q_grids, q_events

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @abstractproperty
    def default_definition(self):
        raise NotImplemented

    @property
    def definition(self):
        return self._definition

    ### PUBLIC METHODS ###

    def find_divisible_leaf_indices(self, leaves):
        indices = []
        for i, leaf in enumerate(leaves):
            if leaf.is_divisible and len(leaf.q_events):
                indices.append(i)
        return indices

    @abstractmethod
    def find_leaf_subdivisions(self, leaf):
        raise NotImplemented

    @abstractmethod
    def is_valid_definition(self, definition):
        raise NotImplemented

    def make_definition_immutable(self, definition):
        pass
        
