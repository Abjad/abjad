# -*- encoding: utf-8 -*-
import abc
import copy
import types
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class IncisedRhythmMaker(RhythmMaker):
    '''Abstract base class for rhythm-makers that incise some or
    all of the output cells they produce.

    Rhythm makers can incise the edge of every output cell.

    Or rhythm-makers can incise only the start of the first output cell
    and the end of the last output cell.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [8],
        [1, 2, 3, 4],
        [1],
        [1],
        32,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        prefix_talea=None,
        prefix_lengths=None,
        suffix_talea=None,
        suffix_lengths=None,
        talea_denominator=None,
        body_ratio=None,
        prolation_addenda=None,
        secondary_divisions=None,
        prefix_talea_helper=None,
        prefix_lengths_helper=None,
        suffix_talea_helper=None,
        suffix_lengths_helper=None,
        prolation_addenda_helper=None,
        secondary_divisions_helper=None,
        decrease_durations_monotonically=True,
        tie_rests=False,
        forbidden_written_duration=None,
        beam_each_cell=False,
        beam_cells_together=False,
        ):
        RhythmMaker.__init__(
            self,
            forbidden_written_duration=forbidden_written_duration,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together,
            )
        prolation_addenda = \
            self._none_to_new_list(prolation_addenda)
        secondary_divisions = \
            self._none_to_new_list(secondary_divisions)
        prefix_talea_helper = \
            self._none_to_trivial_helper(prefix_talea_helper)
        prefix_lengths_helper = \
            self._none_to_trivial_helper(prefix_lengths_helper)
        suffix_talea_helper = \
            self._none_to_trivial_helper(suffix_talea_helper)
        suffix_lengths_helper = \
            self._none_to_trivial_helper(suffix_lengths_helper)
        prolation_addenda_helper = \
            self._none_to_trivial_helper(prolation_addenda_helper)
        secondary_divisions_helper = \
            self._none_to_trivial_helper(secondary_divisions_helper)
        assert sequencetools.all_are_integer_equivalent_numbers(
            prefix_talea), prefix_talea
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prefix_lengths), prefix_lengths
        assert sequencetools.all_are_integer_equivalent_numbers(
            suffix_talea), suffix_talea
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            suffix_lengths), suffix_lengths
        assert mathtools.is_positive_integer_equivalent_number(
            talea_denominator), talea_denominator
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prolation_addenda), prolation_addenda
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            secondary_divisions), secondary_divisions
        assert isinstance(
            prefix_talea_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            prefix_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            suffix_talea_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            suffix_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            prolation_addenda_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            secondary_divisions_helper, (types.FunctionType, types.MethodType))
        assert isinstance(
            decrease_durations_monotonically, bool)
        assert isinstance(
            tie_rests, bool)
        self.prefix_talea = prefix_talea
        self.prefix_lengths = prefix_lengths
        self.suffix_talea = suffix_talea
        self.suffix_lengths = suffix_lengths
        self.prolation_addenda = prolation_addenda
        self.talea_denominator = talea_denominator
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self.body_ratio = body_ratio
        self.secondary_divisions = secondary_divisions
        self.prefix_talea_helper = \
            self._none_to_trivial_helper(prefix_talea_helper)
        self.prefix_lengths_helper = \
            self._none_to_trivial_helper(prefix_lengths_helper)
        self.suffix_talea_helper = \
            self._none_to_trivial_helper(suffix_talea_helper)
        self.suffix_lengths_helper = \
            self._none_to_trivial_helper(suffix_lengths_helper)
        self.prolation_addenda_helper = \
            self._none_to_trivial_helper(prolation_addenda_helper)
        self.secondary_divisions_helper = \
            self._none_to_trivial_helper(secondary_divisions_helper)
        self.decrease_durations_monotonically = \
            decrease_durations_monotonically
        self.tie_rests = tie_rests

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls incised rhythm-maker on `divisions`.

        Returns list of tuplets or return list of leaf lists.
        '''
        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
        result = self._prepare_input(seeds)
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths = \
            result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        talee = (
            prefix_talea, suffix_talea, prolation_addenda, secondary_divisions)
        result = self._scale_talee(
            duration_pairs, self.talea_denominator, talee)
        duration_pairs, lcd, prefix_talea, suffix_talea = result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        if getattr(self, '_is_division_incised', False):
            numeric_map = self._make_division_incised_numeric_map(
                secondary_duration_pairs,
                prefix_talea,
                prefix_lengths,
                suffix_talea,
                suffix_lengths,
                prolation_addenda,
                )
        else:
            assert getattr(self, '_is_output_incised', False)
            numeric_map = self._make_output_incised_numeric_map(
                secondary_duration_pairs,
                prefix_talea,
                prefix_lengths,
                suffix_talea,
                suffix_lengths,
                prolation_addenda,
                )
        leaf_lists = self._numeric_map_and_talea_denominator_to_leaf_lists(
            numeric_map, lcd)
        if not self.prolation_addenda:
            result = leaf_lists
        else:
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            result = tuplets
        assert self._all_are_tuplets_or_all_are_leaf_lists(
            result), repr(result)
        return result

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _make_middle_of_numeric_map_part(self, middle):
        pass

    def _make_division_incised_numeric_map(
        self, 
        duration_pairs=None,
        prefix_talea=None, 
        prefix_lengths=None,
        suffix_talea=None, 
        suffix_lengths=None, 
        prolation_addenda=None,
        ):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        for pair_index, duration_pair in enumerate(duration_pairs):
            prefix_length, suffix_length = \
                prefix_lengths[pair_index], suffix_lengths[pair_index]
            prefix = prefix_talea[
                prefix_talea_index:prefix_talea_index+prefix_length]
            suffix = suffix_talea[
                suffix_talea_index:suffix_talea_index+suffix_length]
            prefix_talea_index += prefix_length
            suffix_talea_index += suffix_length
            prolation_addendum = prolation_addenda[pair_index]
            if isinstance(duration_pair, tuple):
                numerator = duration_pair[0] + (
                    prolation_addendum % duration_pair[0])
            else:
                numerator = duration_pair.numerator + (
                    prolation_addendum % duration_pair.numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map

    def _make_numeric_map_part(
        self,
        numerator,
        prefix,
        suffix,
        is_note_filled=True,
        ):
        prefix_weight = mathtools.weight(prefix)
        suffix_weight = mathtools.weight(suffix)
        middle = numerator - prefix_weight - suffix_weight
        if numerator < prefix_weight:
            weights = [numerator]
            prefix = sequencetools.split_sequence_by_weights(
                prefix, weights, cyclic=False, overhang=False)[0]
        middle = self._make_middle_of_numeric_map_part(middle)
        suffix_space = numerator - prefix_weight
        if suffix_space <= 0:
            suffix = ()
        elif suffix_space < suffix_weight:
            weights = [suffix_space]
            suffix = sequencetools.split_sequence_by_weights(
                suffix, weights, cyclic=False, overhang=False)[0]
        numeric_map_part = prefix + middle + suffix
        return numeric_map_part

    def _make_output_incised_numeric_map(
        self,
        duration_pairs,
        prefix_talea,
        prefix_lengths,
        suffix_talea,
        suffix_lengths,
        prolation_addenda,
        ):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        prefix_length, suffix_length = prefix_lengths[0], suffix_lengths[0]
        prefix = prefix_talea[
            prefix_talea_index:prefix_talea_index+prefix_length]
        suffix = suffix_talea[
            suffix_talea_index:suffix_talea_index+suffix_length]
        if len(duration_pairs) == 1:
            prolation_addendum = prolation_addenda[0]
            if isinstance(duration_pairs[0], mathtools.NonreducedFraction):
                numerator = duration_pairs[0].numerator
            else:
                numerator = duration_pairs[0][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        else:
            prolation_addendum = prolation_addenda[0]
            if isinstance(duration_pairs[0], tuple):
                numerator = duration_pairs[0][0]
            else:
                numerator = duration_pairs[0].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, ())
            numeric_map.append(numeric_map_part)
            for i, duration_pair in enumerate(duration_pairs[1:-1]):
                prolation_addendum = prolation_addenda[i+1]
                if isinstance(duration_pair, tuple):
                    numerator = duration_pair[0]
                else:
                    numerator = duration_pair.numerator
                numerator += (prolation_addendum % numerator)
                numeric_map_part = self._make_numeric_map_part(
                    numerator, (), ())
                numeric_map.append(numeric_map_part)
            try:
                prolation_addendum = prolation_addenda[i+2]
            except UnboundLocalError:
                prolation_addendum = prolation_addenda[1+2]
            if isinstance(duration_pairs[-1], tuple):
                numerator = duration_pairs[-1][0]
            else:
                numerator = duration_pairs[-1].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, (), suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map

    def _numeric_map_and_talea_denominator_to_leaf_lists(
        self, numeric_map, lcd):
        leaf_lists = []
        for numeric_map_part in numeric_map:
            leaf_list = scoretools.make_leaves_from_talea(
                numeric_map_part,
                lcd,
                forbidden_written_duration=self.forbidden_written_duration,
                decrease_durations_monotonically=self.decrease_durations_monotonically,
                tie_rests=self.tie_rests,
                )
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _prepare_input(self, seeds):
        prefix_talea = \
            self.prefix_talea_helper(self.prefix_talea, seeds)
        prefix_lengths = \
            self.prefix_lengths_helper(self.prefix_lengths, seeds)
        suffix_talea = \
            self.suffix_talea_helper(self.suffix_talea, seeds)
        suffix_lengths = \
            self.suffix_lengths_helper(self.suffix_lengths, seeds)
        prolation_addenda = \
            self.prolation_addenda_helper(self.prolation_addenda, seeds)
        secondary_divisions = \
            self.secondary_divisions_helper(self.secondary_divisions, seeds)
        prefix_talea = datastructuretools.CyclicTuple(prefix_talea)
        suffix_talea = datastructuretools.CyclicTuple(suffix_talea)
        prefix_lengths = datastructuretools.CyclicTuple(prefix_lengths)
        suffix_lengths = datastructuretools.CyclicTuple(suffix_lengths)
        if prolation_addenda:
            prolation_addenda = datastructuretools.CyclicTuple(prolation_addenda)
        else:
            prolation_addenda = datastructuretools.CyclicTuple([0])
        secondary_divisions = datastructuretools.CyclicTuple(secondary_divisions)
        return (
            prefix_talea,
            prefix_lengths,
            suffix_talea,
            suffix_lengths,
            prolation_addenda,
            secondary_divisions,
            )

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses incised rhythm-maker.

        Returns newly constructed rhythm-maker.
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
