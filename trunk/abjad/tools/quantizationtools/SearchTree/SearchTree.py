import abc
import copy
import inspect
import pprint
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class SearchTree(AbjadObject):
    '''Abstract base class from which concrete ``SearchTree`` subclasses inherit.

    ``SearchTrees`` encapsulate strategies for generating collections of ``QGrids``,
    given a set of ``QEventProxy`` instances as input.

    They allow composers to define the degree and quality of nested rhythmic
    subdivisions in the quantization output.  That is to say, they allow composers
    to specify what sorts of tuplets and ratios of pulses may be contained within
    other tuplets, to arbitrary levels of nesting.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_definition',)

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self._is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
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

    def __eq__(self, other):
        if type(self) == type(other):
            if self.definition == other.definition:
                return True
        return False

    def __getnewargs__(self):
        return (self.definition,)

    def __getstate__(self):
        state = {}
        for klass in inspect.getmro(self.__class__):  
            if hasattr(klass, '__slots__'):
                for slot in klass.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state
    
    def __repr__(self):
        result = ['{}('.format(self._class_name)]
        definition = pprint.pformat(self.definition, indent=4, width=64).splitlines()
        result.append('\tdefinition={}'.format(definition[0]))
        result.extend(['\t' + x for x in definition[1:]])
        result.append('\t)')
        return '\n'.join(result)

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def default_definition(self):
        '''The default search tree definition.

        Return dictionary.
        '''
        raise NotImplemented

    @property
    def definition(self):
        '''The search tree definition.

        Return dictionary.
        '''
        return copy.deepcopy(self._definition)

    ### PRIVATE METHODS ###

    def _find_divisible_leaf_indices_and_subdivisions(self, q_grid):
        # TODO: This should actually check for all QEvents which fall within the leaf's duration,
        # including QEvents attached to the next leaf
        # It may be prudent to actually store QEvents in two lists: before_offset and after_offset
        indices, subdivisions = [], []

        leaves = q_grid.leaves
        i = 0
        for leaf_one, leaf_two in sequencetools.iterate_sequence_pairwise_strict(leaves):
            if (leaf_one.succeeding_q_event_proxies or leaf_two.preceding_q_event_proxies) \
                and leaf_one.is_divisible:
                if len(leaf_one.q_event_proxies) == 1 and leaf_one.q_event_proxies[0].offset == leaf_one.start_offset:
                    pass # a perfect match, don't bother to continue subdivision
                else:
                    parentage_ratios = leaf_one.parentage_ratios
                    leaf_subdivisions = self._find_leaf_subdivisions(parentage_ratios)
                    if leaf_subdivisions:
                        indices.append(i)
                        subdivisions.append(tuple(leaf_subdivisions))
            i += 1
        return indices, subdivisions

    @abc.abstractmethod
    def _find_leaf_subdivisions(self, leaf):
        raise NotImplemented

    def _generate_all_subdivision_commands(self, q_grid):
        indices, subdivisions = self._find_divisible_leaf_indices_and_subdivisions(q_grid)
        if not indices:
            return ()
        combinations = [tuple(x) for x in sequencetools.yield_outer_product_of_sequences(subdivisions)]
        return tuple(tuple(zip(indices, combo)) for combo in combinations)

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        indent = '\t'
        if not is_indented:
            indent = ''
        result = ['{}('.format(self._tools_package_qualified_class_name)]
        definition = pprint.pformat(self.definition, indent=4, width=64).splitlines()
        result.append('{}definition={}'.format(indent, definition[0]))
        result.extend([indent + x for x in definition[1:]])
        result.append('{})'.format(indent))
        return result

    @abc.abstractmethod
    def _is_valid_definition(self, definition):
        raise NotImplemented
