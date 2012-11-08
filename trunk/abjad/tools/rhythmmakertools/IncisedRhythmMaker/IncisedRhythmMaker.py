import abc
import copy
import types
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class IncisedRhythmMaker(RhythmMaker):
    '''.. versionadded 2.8

    Abstract base class for rhythm-makers that incise some or 
    all of the output cells they produce.

    Rhythm makers can incise the edge of every output cell.
    
    Or rhythm-makers can incise only the start of the first output cell 
    and the end of the last output cell.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    _default_mandatory_input_arguments = (
        [8],
        [1, 2, 3, 4],
        [1],
        [1],
        32,
        )

    ### INITIALIZER ###

    def __init__(self, prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, talea_denominator,
        prolation_addenda=None, secondary_divisions=None,
        prefix_talea_helper=None, prefix_lengths_helper=None,
        suffix_talea_helper=None, suffix_lengths_helper=None,
        prolation_addenda_helper=None, secondary_divisions_helper=None,
        decrease_durations_monotonically=True, tie_rests=False
        ):
        RhythmMaker.__init__(self)
        prolation_addenda = self._none_to_new_list(prolation_addenda)
        secondary_divisions = self._none_to_new_list(secondary_divisions)
        prefix_talea_helper = self._none_to_trivial_helper(prefix_talea_helper)
        prefix_lengths_helper = self._none_to_trivial_helper(prefix_lengths_helper)
        suffix_talea_helper = self._none_to_trivial_helper(suffix_talea_helper)
        suffix_lengths_helper = self._none_to_trivial_helper(suffix_lengths_helper)
        prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(secondary_divisions_helper)
        assert sequencetools.all_are_integer_equivalent_numbers(prefix_talea)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(prefix_lengths)
        assert sequencetools.all_are_integer_equivalent_numbers(suffix_talea)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(suffix_lengths)
        assert mathtools.is_positive_integer_equivalent_number(talea_denominator)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(secondary_divisions)
        assert isinstance(prefix_talea_helper, (types.FunctionType, types.MethodType))
        assert isinstance(prefix_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(suffix_talea_helper, (types.FunctionType, types.MethodType))
        assert isinstance(suffix_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(prolation_addenda_helper, (types.FunctionType, types.MethodType))
        assert isinstance(secondary_divisions_helper, (types.FunctionType, types.MethodType))
        assert isinstance(decrease_durations_monotonically, bool)
        assert isinstance(tie_rests, bool)
        self.prefix_talea = prefix_talea
        self.prefix_lengths = prefix_lengths
        self.suffix_talea = suffix_talea
        self.suffix_lengths = suffix_lengths
        self.prolation_addenda = prolation_addenda
        self.talea_denominator = talea_denominator
        self.secondary_divisions = secondary_divisions
        self.prefix_talea_helper = self._none_to_trivial_helper(prefix_talea_helper)
        self.prefix_lengths_helper = self._none_to_trivial_helper(prefix_lengths_helper)
        self.suffix_talea_helper = self._none_to_trivial_helper(suffix_talea_helper)
        self.suffix_lengths_helper = self._none_to_trivial_helper(suffix_lengths_helper)
        self.prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
        self.secondary_divisions_helper = self._none_to_trivial_helper(secondary_divisions_helper)
        self.decrease_durations_monotonically = decrease_durations_monotonically
        self.tie_rests = tie_rests

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
        result = self._prepare_input(seeds)
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths = result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        talee = (prefix_talea, suffix_talea, prolation_addenda, secondary_divisions)
        result = self._scale_talee(duration_pairs, self.talea_denominator, talee)
        duration_pairs, lcd, prefix_talea, suffix_talea = result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        numeric_map = self._make_numeric_map(secondary_duration_pairs,
            prefix_talea, prefix_lengths, suffix_talea, suffix_lengths, prolation_addenda)
        leaf_lists = self._numeric_map_and_talea_denominator_to_leaf_lists(numeric_map, lcd)
        if not self.prolation_addenda:
            return leaf_lists
        else:
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            return tuplets

    def __eq__(self, other):
        return isinstance(other, type(self)) and all([
            self.prefix_talea == other.prefix_talea,
            self.prefix_lengths == other.prefix_lengths,
            self.suffix_talea == other.suffix_talea,
            self.suffix_lengths == other.suffix_lengths,
            self.prolation_addenda == other.prolation_addenda,
            self.talea_denominator == other.talea_denominator,
            self.secondary_divisions == other.secondary_divisions,
            ])

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _make_middle_of_numeric_map_part(self, middle):
        pass

    def _make_numeric_map_part(self, numerator, prefix, suffix, is_note_filled=True):
        prefix_weight = mathtools.weight(prefix)
        suffix_weight = mathtools.weight(suffix)
        middle = numerator - prefix_weight - suffix_weight
        if numerator < prefix_weight:
            weights = [numerator]
            prefix = sequencetools.split_sequence_by_weights(prefix, weights, cyclic=False, overhang=False)[0]
        middle = self._make_middle_of_numeric_map_part(middle)
        suffix_space = numerator - prefix_weight
        if suffix_space <= 0:
            suffix = ()
        elif suffix_space < suffix_weight:
            weights = [suffix_space]
            suffix = sequencetools.split_sequence_by_weights(suffix, weights, cyclic=False, overhang=False)[0]
        numeric_map_part = prefix + middle + suffix
        return numeric_map_part

    def _numeric_map_and_talea_denominator_to_leaf_lists(self, numeric_map, lcd):
        leaf_lists = []
        for numeric_map_part in numeric_map:
            leaf_list = leaftools.make_leaves_from_talea(
                numeric_map_part, lcd,
                decrease_durations_monotonically=self.decrease_durations_monotonically, tie_rests=self.tie_rests)
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _prepare_input(self, seeds):
        prefix_talea = self.prefix_talea_helper(self.prefix_talea, seeds)
        prefix_lengths = self.prefix_lengths_helper(self.prefix_lengths, seeds)
        suffix_talea = self.suffix_talea_helper(self.suffix_talea, seeds)
        suffix_lengths = self.suffix_lengths_helper(self.suffix_lengths, seeds)
        prolation_addenda = self.prolation_addenda_helper(self.prolation_addenda, seeds)
        secondary_divisions = self.secondary_divisions_helper(self.secondary_divisions, seeds)
        prefix_talea = sequencetools.CyclicTuple(prefix_talea)
        suffix_talea = sequencetools.CyclicTuple(suffix_talea)
        prefix_lengths = sequencetools.CyclicTuple(prefix_lengths)
        suffix_lengths = sequencetools.CyclicTuple(suffix_lengths)
        if prolation_addenda:
            prolation_addenda = sequencetools.CyclicTuple(prolation_addenda)
        else:
            prolation_addenda = sequencetools.CyclicTuple([0])
        secondary_divisions = sequencetools.CyclicTuple(secondary_divisions)
        return prefix_talea, prefix_lengths, \
            suffix_talea, suffix_lengths, prolation_addenda, secondary_divisions

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''.. versionadded:: 2.10

        Reverse incised rhythm-maker.

        Return newly constructed rhythm-maker.
        '''
        new = copy.deepcopy(self)
        new.prefix_talea.reverse()
        new.prefix_lengths.reverse()
        new.suffix_talea.reverse()
        new.suffix_lengths.reverse()
        new.prolation_addenda.reverse()
        new.secondary_divisions.reverse()
        if new.decrease_durations_monotonically:
            new.decrease_durations_monotonically = False
        return new
