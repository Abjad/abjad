# -*- encoding: utf-8 -*-
import abc
import copy
import inspect
import pprint
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class SearchTree(AbjadObject):
    r'''Abstract base class from which concrete ``SearchTree`` subclasses 
    inherit.

    ``SearchTrees`` encapsulate strategies for generating collections of 
    ``QGrids``, given a set of ``QEventProxy`` instances as input.

    They allow composers to define the degree and quality of nested rhythmic
    subdivisions in the quantization output.  That is to say, they allow 
    composers to specify what sorts of tuplets and ratios of pulses may be 
    contained within other tuplets, to arbitrary levels of nesting.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_definition',
        )

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self._is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
        r'''Calls search tree.
        '''
        from abjad.tools import quantizationtools
        assert isinstance(q_grid, quantizationtools.QGrid)
        new_q_grids = []
        commands = self._generate_all_subdivision_commands(q_grid)
        for command in commands:
            new_q_grid = copy.copy(q_grid)
            q_events = new_q_grid.subdivide_leaves(command)
            new_q_grid.fit_q_events(q_events)
            new_q_grids.append(new_q_grid)
        return new_q_grids

    def __eq__(self, expr):
        r'''True when `expr` is a search tree with definition equal to that of
        this search tree. Otherwise false.

        Returns boolean.
        '''
        if type(self) == type(expr):
            if self.definition == expr.definition:
                return True
        return False

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.definition,)

    def __getstate__(self):
        r'''Gets state of search tree.

        Returns dictionary.
        '''
        state = {}
        for current_class in inspect.getmro(type(self)):
            if hasattr(current_class, '__slots__'):
                for slot in current_class.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __setstate__(self, state):
        r'''Sets `state` of search tree.

        Returns none.
        '''
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _find_divisible_leaf_indices_and_subdivisions(self, q_grid):
        # TODO: This should actually check for all QEvents which fall 
        # within the leaf's duration,
        # including QEvents attached to the next leaf
        # It may be prudent to actually store QEvents in two lists: 
        # before_offset and after_offset
        indices, subdivisions = [], []

        leaves = q_grid.leaves
        i = 0
        for leaf_one, leaf_two in \
            sequencetools.iterate_sequence_pairwise_strict(leaves):
            if (leaf_one.succeeding_q_event_proxies or 
                leaf_two.preceding_q_event_proxies) and \
                leaf_one.is_divisible:
                if len(leaf_one.q_event_proxies) == 1 and \
                    leaf_one.q_event_proxies[0].offset == \
                        leaf_one.start_offset:
                    pass # perfect match, don't bother to continue subdivision
                else:
                    parentage_ratios = leaf_one.parentage_ratios
                    leaf_subdivisions = \
                        self._find_leaf_subdivisions(parentage_ratios)
                    if leaf_subdivisions:
                        indices.append(i)
                        subdivisions.append(tuple(leaf_subdivisions))
            i += 1
        return indices, subdivisions

    @abc.abstractmethod
    def _find_leaf_subdivisions(self, leaf):
        raise NotImplemented

    def _generate_all_subdivision_commands(self, q_grid):
        indices, subdivisions = \
            self._find_divisible_leaf_indices_and_subdivisions(q_grid)
        if not indices:
            return ()
        combinations = [tuple(x) 
            for x in sequencetools.yield_outer_product_of_sequences(
            subdivisions)]
        return tuple(tuple(zip(indices, combo)) for combo in combinations)

    @abc.abstractmethod
    def _is_valid_definition(self, definition):
        raise NotImplemented

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def default_definition(self):
        r'''The default search tree definition.

        Returns dictionary.
        '''
        raise NotImplemented

    @property
    def definition(self):
        r'''The search tree definition.

        Returns dictionary.
        '''
        return copy.deepcopy(self._definition)
