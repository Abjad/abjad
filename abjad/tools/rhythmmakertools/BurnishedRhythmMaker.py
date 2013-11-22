# -*- encoding: utf-8 -*-
import abc
import copy
import types
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate


class BurnishedRhythmMaker(RhythmMaker):
    '''Abstract base class for rhythm-makers that burnish some or
    all of the output cells they produce.

    'Burnishing' means to forcibly cast the first or last
    (or both first and last) elements of a output cell to be
    either a note or rest.

    'Division-burnishing' rhythm-makers burnish every output cell they 
    produce.

    'Output-burnishing' rhythm-makers burnish only the first and last
    output cells they produce and leave interior output cells unchanged.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [-1, 4, -2, 3], 
        16,
        )

    ### INITIALIZER ###

    def __init__(self, 
        talea=None, 
        talea_denominator=None, 
        prolation_addenda=None,
        lefts=None, 
        middles=None, 
        rights=None, 
        left_lengths=None, 
        right_lengths=None,
        secondary_divisions=None,
        talea_helper=None, 
        prolation_addenda_helper=None,
        lefts_helper=None, 
        middles_helper=None, 
        rights_helper=None,
        left_lengths_helper=None, 
        right_lengths_helper=None, 
        secondary_divisions_helper=None,
        beam_each_cell=False, 
        beam_cells_together=False,
        decrease_durations_monotonically=True, 
        tie_split_notes=False, 
        tie_rests=False,
        ):
        RhythmMaker.__init__(self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together,
            )
        prolation_addenda = self._none_to_new_list(prolation_addenda)
        lefts = self._none_to_new_list(lefts)
        middles = self._none_to_new_list(middles)
        rights = self._none_to_new_list(rights)
        left_lengths = self._none_to_new_list(left_lengths)
        right_lengths = self._none_to_new_list(right_lengths)
        secondary_divisions = self._none_to_new_list(secondary_divisions)
        talea_helper = self._none_to_trivial_helper(talea_helper)
        prolation_addenda_helper = self._none_to_trivial_helper(
            prolation_addenda_helper)
        lefts_helper = self._none_to_trivial_helper(lefts_helper)
        middles_helper = self._none_to_trivial_helper(middles_helper)
        rights_helper = self._none_to_trivial_helper(rights_helper)
        left_lengths_helper = self._none_to_trivial_helper(
            left_lengths_helper)
        right_lengths_helper = self._none_to_trivial_helper(
            right_lengths_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(
            secondary_divisions_helper)
        assert sequencetools.all_are_integer_equivalent_numbers(talea)
        assert mathtools.is_positive_integer_equivalent_number(
            talea_denominator)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prolation_addenda)
        assert all(x in (-1, 0, 1) for x in lefts)
        assert all(x in (-1, 0, 1) for x in middles)
        assert all(x in (-1, 0, 1) for x in rights)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            left_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            right_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            secondary_divisions)
        assert isinstance(talea_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(prolation_addenda_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(lefts_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(middles_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(rights_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(left_lengths_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(right_lengths_helper, 
            (types.FunctionType, types.MethodType))
        assert isinstance(decrease_durations_monotonically, bool)
        assert isinstance(tie_split_notes, bool)
        assert isinstance(tie_rests, bool)
        self.talea = talea
        self.talea_denominator = talea_denominator
        self.prolation_addenda = prolation_addenda
        self.lefts = lefts
        self.middles = middles
        self.rights = rights
        self.left_lengths = left_lengths
        self.right_lengths = right_lengths
        self.secondary_divisions = secondary_divisions
        self.talea_helper = talea_helper
        self.prolation_addenda_helper = prolation_addenda_helper
        self.lefts_helper = lefts_helper
        self.middles_helper = middles_helper
        self.rights_helper = rights_helper
        self.left_lengths_helper = left_lengths_helper
        self.right_lengths_helper = right_lengths_helper
        self.secondary_divisions_helper = secondary_divisions_helper
        #self.beam_each_cell = beam_each_cell
        self.decrease_durations_monotonically = \
            decrease_durations_monotonically
        self.tie_split_notes = tie_split_notes
        self.tie_rests = tie_rests

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls burnished rhythm-maker on `divisions`.

        Returns either list of tuplets or else list of note-lists.
        '''
        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
        octuplet = self._prepare_input(seeds)
        talea, prolation_addenda = octuplet[:2]
        secondary_divisions = octuplet[-1]
        talee = (talea, prolation_addenda, secondary_divisions)
        result = self._scale_talee(
            duration_pairs, self.talea_denominator, talee)
        duration_pairs, lcd, talea, prolation_addenda, secondary_divisions = \
            result
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        septuplet = (talea, prolation_addenda) + octuplet[2:-1]
        numeric_map = self._make_numeric_map(
            secondary_duration_pairs, septuplet)
        leaf_lists = self._make_leaf_lists(numeric_map, lcd)
        if not prolation_addenda:
            result = leaf_lists
        else:
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            result = tuplets
        if self.beam_each_cell:
            for cell in result:
                beam = spannertools.MultipartBeam()
                attach(beam, cell)
        if self.tie_split_notes:
            self._add_ties(result)
        assert isinstance(result, list), repr(result)
        assert all(isinstance(x, selectiontools.Selection) for x in result) or \
            all(isinstance(x, scoretools.Tuplet) for x in result)
        return result

    def __format__(self, format_specification=''):
        r'''Formats burnished rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(BurnishedRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _add_ties(self, result):
        from abjad.tools import selectiontools
        leaves = list(iterate(result).by_class(scoretools.Leaf))
        written_durations = [leaf.written_duration for leaf in leaves]
        weights = [durationtools.Duration(numerator, self.talea_denominator) 
            for numerator in self.talea]
        parts = sequencetools.partition_sequence_by_weights_exactly(
            written_durations, weights=weights, cyclic=True, overhang=True)
        counts = [len(part) for part in parts]
        parts = sequencetools.partition_sequence_by_counts(leaves, counts)
        prototype = (spannertools.Tie,)
        for part in parts:
            part = selectiontools.SliceSelection(part)
            tie_spanner = spannertools.Tie()
            # this is voodoo to temporarily neuter the contiguity constraint
            tie_spanner._contiguity_constraint = None
            for component in part:
                # TODO: make top-level detach() work here
                for spanner in component._get_spanners(
                    prototype=prototype):
                    spanner.detach()
                #detach(prototype, component)
            tie_spanner.extend(part)

    def _burnish_division_part(self, division_part, token):
        assert len(division_part) == len(token)
        new_division_part = []
        for number, i in zip(division_part, token):
            if i == -1:
                new_division_part.append(-abs(number))
            elif i == 0:
                new_division_part.append(number)
            elif i == 1:
                new_division_part.append(abs(number))
            else:
                raise ValueError
        new_division_part = type(division_part)(new_division_part)
        return new_division_part

    @abc.abstractmethod
    def _burnish_division_parts(self, divisions, quintuplet):
        pass

    def _make_leaf_lists(self, numeric_map, talea_denominator):
        leaf_lists = []
        for map_division in numeric_map:
            leaf_list = scoretools.make_leaves_from_talea(
                map_division, talea_denominator,
                decrease_durations_monotonically=self.decrease_durations_monotonically,
                tie_rests=self.tie_rests)
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _make_numeric_map(self, duration_pairs, septuplet):
        talea, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
        prolated_duration_pairs = self._make_prolated_duration_pairs(
            duration_pairs, prolation_addenda)
        if isinstance(prolated_duration_pairs[0], tuple):
            prolated_numerators = [
                pair[0] for pair in prolated_duration_pairs]
        else:
            prolated_numerators = [
                pair.numerator for pair in prolated_duration_pairs]
        map_divisions = sequencetools.split_sequence_extended_to_weights(
            talea, prolated_numerators, overhang=False)
        quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
        burnished_map_divisions = self._burnish_division_parts(
            map_divisions, quintuplet)
        numeric_map = burnished_map_divisions
        return numeric_map

    def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
        prolated_duration_pairs = []
        for i, duration_pair in enumerate(duration_pairs):
            if not prolation_addenda:
                prolated_duration_pairs.append(duration_pair)
            else:
                prolation_addendum = prolation_addenda[i]
                if hasattr(duration_pair, 'numerator'):
                    prolation_addendum %= duration_pair.numerator
                else:
                    prolation_addendum %= duration_pair[0]
                if isinstance(duration_pair, tuple):
                    numerator, denominator = duration_pair
                else:
                    numerator, denominator = duration_pair.pair
                prolated_duration_pair = (
                    numerator + prolation_addendum, denominator)
                prolated_duration_pairs.append(prolated_duration_pair)
        return prolated_duration_pairs

    def _prepare_input(self, seeds):
        talea = datastructuretools.CyclicTuple(self.talea_helper(self.talea, seeds))
        prolation_addenda = \
            self.prolation_addenda_helper(self.prolation_addenda, seeds)
        prolation_addenda = datastructuretools.CyclicTuple(prolation_addenda)
        lefts = datastructuretools.CyclicTuple(self.lefts_helper(self.lefts, seeds))
        middles = datastructuretools.CyclicTuple(
            self.middles_helper(self.middles, seeds))
        rights = datastructuretools.CyclicTuple(
            self.rights_helper(self.rights, seeds))
        left_lengths = datastructuretools.CyclicTuple(
            self.left_lengths_helper(self.left_lengths, seeds))
        right_lengths = datastructuretools.CyclicTuple(
            self.right_lengths_helper(self.right_lengths, seeds))
        secondary_divisions = self.secondary_divisions_helper(
            self.secondary_divisions, seeds)
        secondary_divisions = datastructuretools.CyclicTuple(
            secondary_divisions)
        return (
            talea,
            prolation_addenda,
            lefts, 
            middles, 
            rights, 
            left_lengths, 
            right_lengths, 
            secondary_divisions,
            )

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses burnished rhythm-maker.

        Defined equal to a copy of rhythm-maker with all the following
        lists reversed:

        ::

            new.talea
            new.prolation_addenda
            new.lefts
            new.middles
            new.rights
            new.left_lengths
            new.right_lengths
            new.secondary_divisions

        Returns newly constructed rhythm-maker.
        '''
        new = copy.deepcopy(self)
        new.talea.reverse()
        new.prolation_addenda.reverse()
        new.lefts.reverse()
        new.middles.reverse()
        new.rights.reverse()
        new.left_lengths.reverse()
        new.right_lengths.reverse()
        new.secondary_divisions.reverse()
        if new.decrease_durations_monotonically:
            new.decrease_durations_monotonically = False
        return new
