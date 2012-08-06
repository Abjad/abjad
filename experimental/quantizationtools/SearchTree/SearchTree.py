from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from experimental.quantizationtools.QGrid import QGrid
import copy


class SearchTree(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_definition',)

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self.is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
        assert isinstance(q_grid, QGrid)
        new_q_grids = []
        commands = self.generate_all_subdivision_commands(q_grid)
        for command in commands:
            new_q_grid = copy.copy(q_grid)
            q_events = new_q_grid.subdivide_leaves(command)
            new_q_grid.fit_q_events(q_events)
            new_q_grids.append(new_q_grid)
        return new_q_grids

    def __eq__(self, other):
        if type(self) == type(other):
            if self.definition == other.definition:
                return True
        return False

    def __getnewargs__(self):
        return self.definition

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @abstractproperty
    def default_definition(self):
        raise NotImplemented

    @property
    def definition(self):
        return copy.deepcopy(self._definition)

    ### PUBLIC METHODS ###

    def generate_all_subdivision_commands(self, q_grid):
        indices, subdivisions = self.find_divisible_leaf_indices_and_subdivisions(q_grid)
        if not indices:
            return ()
        combinations = [tuple(x) for x in sequencetools.yield_outer_product_of_sequences(subdivisions)]
        return tuple(tuple(zip(indices, combo)) for combo in combinations)

    def find_divisible_leaf_indices_and_subdivisions(self, q_grid):
        # TODO: This should actually check for all QEvents which fall within the leaf's duration,
        # including QEvents attached to the next leaf
        # It may be prudent to actually store QEvents in two lists: before_offset and after_offset
        indices, subdivisions = [], []

        leaves = q_grid.leaves
        i = 0
        for leaf_one, leaf_two in sequencetools.iterate_sequence_pairwise_strict(leaves):
            if (leaf_one.succeeding_q_event_proxies or leaf_two.preceding_q_event_proxies) \
                and leaf_one.is_divisible:
                if len(leaf_one.q_event_proxies) == 1 and leaf_one.q_event_proxies[0].offset == leaf_one.offset:
                    pass # a perfect match, don't bother to continue subdivision
                else:
                    parentage_ratios = leaf_one.parentage_ratios
                    leaf_subdivisions = self.find_leaf_subdivisions(parentage_ratios)
                    if leaf_subdivisions:
                        indices.append(i)
                        subdivisions.append(tuple(leaf_subdivisions))
            i += 1
        return indices, subdivisions

    @abstractmethod
    def find_leaf_subdivisions(self, leaf):
        raise NotImplemented

    @abstractmethod
    def is_valid_definition(self, definition):
        raise NotImplemented
