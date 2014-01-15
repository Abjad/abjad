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


class TaleaRhythmMaker(RhythmMaker):
    '''Talea rhythm-maker.
    
    'Burnishing' means to forcibly cast the first or last
    (or both first and last) elements of a output cell to be
    either a note or rest.

    'Division-burnishing' rhythm-makers burnish every output cell they 
    produce.

    'Output-burnishing' rhythm-makers burnish only the first and last
    output cells they produce and leave interior output cells unchanged.

    ..  container:: example

        Burnishes output: 

        ::

            >>> maker = rhythmmakertools.TaleaRhythmMaker(
            ...     talea=(1, 2, 3),
            ...     talea_denominator=16,
            ...     prolation_addenda=(0, 2),
            ...     lefts=(-1,),
            ...     middles=(0,),
            ...     rights=(-1,),
            ...     left_lengths=(1,),
            ...     right_lengths=(1,),
            ...     secondary_divisions=(9,),
            ...     beam_each_cell=True,
            ...     burnish_output=True,
            ...     )

        ::

            >>> divisions = [(3, 8), (4, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    '''

    '''Example helpers:

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea at second event of talea;
    # voice 3 starts reading talea at third event of talea;
    # voice 4 starts reading talea at fourth event of talea.
    def helper(talea, seeds):
        assert len(seeds) == 2
        if not talea:
            return talea
        voice_index, measure_index = seeds
        talea = sequencetools.rotate_sequence(talea, -voice_index)
        return talea

    # used in a piece with four voices:
    # voice 1 starts reading talea at beginning of talea;
    # voice 2 starts reading talea 1/4 of way through talea;
    # voice 3 starts reading talea 2/4 of way through talea;
    # voice 4 starts reading talea 3/4 of way through talea.
    def quarter_rotation_helper(talea, seeds):
        assert len(seeds) == 2
        if not talea:
            return talea
        voice_index, measure_index = seeds
        index_of_rotation = -voice_index * (len(talea) // 4)
        index_of_rotation += -4 * measure_index
        talea = sequencetools.rotate_sequence(talea, index_of_rotation)
        return talea
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        talea=(-1, 4, -2, 3),
        talea_denominator=16,
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
        burnish_divisions=False,
        burnish_output=False,
        ):
        RhythmMaker.__init__(
            self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together,
            )
        assert isinstance(burnish_divisions, bool)
        assert isinstance(burnish_output, bool)
        self.burnish_divisions = burnish_divisions
        self.burnish_output = burnish_output
        talea = self._none_to_new_list(talea)
        prolation_addenda = self._none_to_new_list(prolation_addenda)
        lefts = self._none_to_new_list(lefts)
        middles = self._none_to_new_list(middles)
        rights = self._none_to_new_list(rights)
        left_lengths = self._none_to_new_list(left_lengths)
        right_lengths = self._none_to_new_list(right_lengths)
        secondary_divisions = self._none_to_new_list(secondary_divisions)
        assert isinstance(talea, (tuple, type(None)))
        assert isinstance(lefts, (tuple, type(None)))
        assert isinstance(middles, (tuple, type(None)))
        assert isinstance(rights, (tuple, type(None)))
        assert isinstance(left_lengths, (tuple, type(None)))
        assert isinstance(right_lengths, (tuple, type(None)))
        assert isinstance(secondary_divisions, (tuple, type(None))), repr(
            secondary_divisions)
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
        assert prolation_addenda is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prolation_addenda)
        assert lefts is None or all(x in (-1, 0, 1) for x in lefts)
        assert middles is None or all(x in (-1, 0, 1) for x in middles)
        assert rights is None or all(x in (-1, 0, 1) for x in rights)
        assert left_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            left_lengths)
        assert right_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            right_lengths)
        assert secondary_divisions is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            secondary_divisions)
        assert callable(talea_helper)
        assert callable(prolation_addenda_helper)
        assert callable(lefts_helper)
        assert callable(middles_helper)
        assert callable(rights_helper)
        assert callable(left_lengths_helper)
        assert callable(right_lengths_helper)
        assert isinstance(decrease_durations_monotonically, bool)
        assert isinstance(tie_split_notes, bool)
        self.talea = tuple(talea)
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

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls burnished rhythm-maker on `divisions`.

        Returns either list of tuplets or else list of note-lists.
        '''
        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
        octuplet = self._prepare_input(seeds)
        talea, prolation_addenda = octuplet[:2]
        secondary_divisions = octuplet[-1]
        taleas = (talea, prolation_addenda, secondary_divisions)
        result = self._scale_taleas(
            duration_pairs, self.talea_denominator, taleas)
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

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(1, 2, 3),
                    talea_denominator=16,
                    prolation_addenda=(0, 2),
                    lefts=(-1,),
                    middles=(0,),
                    rights=(-1,),
                    left_lengths=(1,),
                    right_lengths=(1,),
                    secondary_divisions=(9,),
                    beam_each_cell=True,
                    beam_cells_together=False,
                    decrease_durations_monotonically=True,
                    tie_split_notes=False,
                    burnish_divisions=False,
                    burnish_output=True,
                    )

        Returns string.
        '''
        superclass = super(TaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new talea rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, secondary_divisions=(10,))

            ::

                >>> print format(new_maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(1, 2, 3),
                    talea_denominator=16,
                    prolation_addenda=(0, 2),
                    lefts=(-1,),
                    middles=(0,),
                    rights=(-1,),
                    left_lengths=(1,),
                    right_lengths=(1,),
                    secondary_divisions=(10,),
                    beam_each_cell=True,
                    beam_cells_together=False,
                    decrease_durations_monotonically=True,
                    tie_split_notes=False,
                    burnish_divisions=False,
                    burnish_output=True,
                    )

            ::

                >>> divisions = [(3, 8), (4, 8)]
                >>> music = new_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new talea rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

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
                    spanner._sever_all_components()
                #detach(prototype, component)
            # TODO: remove usae of Spanner._extend()
            tie_spanner._extend(part)

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

    def _burnish_all_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths=quintuplet
        lefts_index, rights_index = 0, 0
        burnished_divisions = []
        for division_index, division in enumerate(divisions):
            left_length = left_lengths[division_index]
            left = lefts[lefts_index:lefts_index+left_length]
            lefts_index += left_length
            right_length = right_lengths[division_index]
            right = rights[rights_index:rights_index+right_length]
            rights_index += right_length
            available_left_length = len(division)
            left_length = min([left_length, available_left_length])
            available_right_length = len(division) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(division) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[division_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                division, 
                [left_length, middle_length, right_length], 
                cyclic=False, 
                overhang=False,
                )
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    def _burnish_division_parts(self, divisions, quintuplet):
        if self.burnish_divisions or getattr(self, '_burnish_divisions', False):
            return self._burnish_all_division_parts(divisions, quintuplet)
        elif self.burnish_output or getattr(self, '_burnish_output', False):
            return self._burnish_first_and_last_division_parts(
                divisions, quintuplet)
        else:
            return divisions

    def _burnish_first_and_last_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        burnished_divisions = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(divisions) == 1:
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(divisions[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0],
                [left_length, middle_length, right_length], 
                cyclic=False,
                overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        else:
            ## first division
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(divisions[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0], 
                [left_length, middle_length],
                cyclic=False,
                overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            burnished_division = left_part + middle_part
            burnished_divisions.append(burnished_division)
            ## middle divisions
            for division in divisions[1:-1]:
                middle_part = division
                middle = len(division) * [middles[0]]
                middle_part = self._burnish_division_part(middle_part, middle)
                burnished_division = middle_part
                burnished_divisions.append(burnished_division)
            ## last division:
            available_right_length = len(divisions[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[-1], 
                [middle_length, right_length], 
                cyclic=False,
                overhang=False)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions

    def _make_leaf_lists(self, numeric_map, talea_denominator):
        leaf_lists = []
        for map_division in numeric_map:
            leaf_list = scoretools.make_leaves_from_talea(
                map_division, 
                talea_denominator,
                decrease_durations_monotonically= \
                    self.decrease_durations_monotonically,
                )
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
        talea = datastructuretools.CyclicTuple(
            self.talea_helper(self.talea, seeds),
            )
        prolation_addenda = self.prolation_addenda or ()
        prolation_addenda = \
            self.prolation_addenda_helper(prolation_addenda, seeds)
        prolation_addenda = datastructuretools.CyclicTuple(prolation_addenda)
        lefts = self.lefts or ()
        lefts = datastructuretools.CyclicTuple(
            self.lefts_helper(lefts, seeds),
            )
        middles = self.middles or ()
        middles = datastructuretools.CyclicTuple(
            self.middles_helper(middles, seeds))
        rights = self.rights or ()
        rights = datastructuretools.CyclicTuple(
            self.rights_helper(rights, seeds),
            )
        left_lengths = self.left_lengths or ()
        left_lengths = datastructuretools.CyclicTuple(
            self.left_lengths_helper(left_lengths, seeds),
            )
        right_lengths = self.right_lengths or ()
        right_lengths = datastructuretools.CyclicTuple(
            self.right_lengths_helper(right_lengths, seeds),
            )
        secondary_divisions = self.secondary_divisions or ()
        secondary_divisions = self.secondary_divisions_helper(
            secondary_divisions, seeds)
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
        r'''Reverses talea rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.TaleaRhythmMaker(
                    talea=(3, 2, 1),
                    talea_denominator=16,
                    prolation_addenda=(2, 0),
                    lefts=(-1,),
                    middles=(0,),
                    rights=(-1,),
                    left_lengths=(1,),
                    right_lengths=(1,),
                    secondary_divisions=(9,),
                    beam_each_cell=True,
                    beam_cells_together=False,
                    decrease_durations_monotonically=False,
                    tie_split_notes=False,
                    burnish_divisions=False,
                    burnish_output=True,
                    )

            ::

                >>> divisions = [(3, 8), (4, 8)]
                >>> music = reversed_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new talea rhythm-maker.
        '''
        talea = tuple(reversed(self.talea))
        prolation_addenda = self.prolation_addenda
        if prolation_addenda is not None:
            prolation_addenda = tuple(reversed(prolation_addenda))
        lefts = self.lefts
        if lefts is not None:
            lefts = tuple(reversed(lefts))
        middles = self.middles
        if middles is not None:
            middles = tuple(reversed(middles))
        rights = self.rights
        if rights is not None:
            rights = tuple(reversed(rights))
        left_lengths = self.left_lengths
        if left_lengths is not None:
            left_lengths = tuple(reversed(left_lengths))
        right_lengths = self.right_lengths
        if right_lengths is not None:
            right_lengths = tuple(reversed(right_lengths))
        secondary_divisions = self.secondary_divisions
        if secondary_divisions is not None:
            secondary_divisions = tuple(reversed(secondary_divisions))
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        new = type(self)(
            talea=talea,
            talea_denominator=self.talea_denominator,
            prolation_addenda=prolation_addenda,
            lefts=lefts,
            middles=middles,
            rights=rights,
            left_lengths=left_lengths,
            right_lengths=right_lengths,
            secondary_divisions=secondary_divisions,
            talea_helper=self.talea_helper, 
            prolation_addenda_helper=self.prolation_addenda_helper,
            lefts_helper=self.lefts_helper, 
            middles_helper=self.middles_helper, 
            rights_helper=self.rights_helper,
            left_lengths_helper=self.left_lengths_helper, 
            right_lengths_helper=self.right_lengths_helper, 
            secondary_divisions_helper=self.secondary_divisions_helper,
            beam_each_cell=self.beam_each_cell, 
            beam_cells_together=self.beam_cells_together,
            decrease_durations_monotonically=decrease_durations_monotonically, 
            tie_split_notes=self.tie_split_notes, 
            burnish_divisions=self.burnish_divisions,
            burnish_output=self.burnish_output,
            )
        return new
