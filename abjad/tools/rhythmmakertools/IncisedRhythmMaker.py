# -*- encoding: utf-8 -*-
import copy
import types
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class IncisedRhythmMaker(RhythmMaker):
    r'''Incised rhythm-maker.
    
    Rhythm makers can incise the edge of every output cell.

    Or rhythm-makers can incise only the start of the first output cell
    and the end of the last output cell.

    ..  container:: example

        Division-incised notes:

        ::

            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     prefix_talea=(-1,),
            ...     prefix_lengths=(0, 1),
            ...     suffix_talea=(-1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=16,
            ...     fill_with_notes=True,
            ...     incise_divisions=True,
            ...     )

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    '''

    ### INITIALIZER ###

    def __init__(
        self,
        prefix_talea=(8,),
        prefix_lengths=(1, 2, 3, 4),
        suffix_talea=(1,),
        suffix_lengths=(1,),
        talea_denominator=32,
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
        forbidden_written_duration=None,
        beam_each_cell=False,
        beam_cells_together=False,
        fill_with_notes=True,
        incise_divisions=False,
        incise_output=False,
        ):
        RhythmMaker.__init__(
            self,
            forbidden_written_duration=forbidden_written_duration,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together,
            )
        prefix_talea = self._none_to_new_list(prefix_talea)
        prefix_lengths = self._none_to_new_list(prefix_lengths)
        suffix_talea = self._none_to_new_list(suffix_talea)
        suffix_lengths = self._none_to_new_list(suffix_lengths)
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
        assert prefix_talea is None or \
            sequencetools.all_are_integer_equivalent_numbers(
            prefix_talea), prefix_talea
        assert prefix_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prefix_lengths), prefix_lengths
        assert suffix_talea is None or \
            sequencetools.all_are_integer_equivalent_numbers(
            suffix_talea), suffix_talea
        assert suffix_lengths is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            suffix_lengths), suffix_lengths
        assert mathtools.is_positive_integer_equivalent_number(
            talea_denominator), talea_denominator
        assert prolation_addenda is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prolation_addenda), prolation_addenda
        assert secondary_divisions is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            secondary_divisions), secondary_divisions
        assert isinstance(prefix_talea, (tuple, type(None)))
        assert isinstance(prefix_lengths, (tuple, type(None)))
        assert isinstance(suffix_talea, (tuple, type(None)))
        assert isinstance(suffix_lengths, (tuple, type(None)))
        assert isinstance(prolation_addenda, (tuple, type(None)))
        assert callable(prefix_talea_helper)
        assert callable(prefix_lengths_helper)
        assert callable(suffix_talea_helper)
        assert callable(suffix_lengths_helper)
        assert callable(prolation_addenda_helper)
        assert callable(secondary_divisions_helper)
        assert isinstance(decrease_durations_monotonically, bool)
        self.prefix_talea = prefix_talea
        self.prefix_lengths = prefix_lengths
        self.suffix_talea = suffix_talea
        self.suffix_lengths = suffix_lengths
        self.prolation_addenda = prolation_addenda
        self.talea_denominator = talea_denominator
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self._body_ratio = body_ratio
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
        assert isinstance(fill_with_notes, bool)
        self._fill_with_notes = fill_with_notes
        assert isinstance(incise_divisions, bool)
        self._incise_divisions = incise_divisions
        assert isinstance(incise_output, bool)
        self._incise_output = incise_output

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
        taleas = (
            prefix_talea, suffix_talea, prolation_addenda, secondary_divisions)
        result = self._scale_taleas(
            duration_pairs, self.talea_denominator, taleas)
        duration_pairs, lcd, prefix_talea, suffix_talea = result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        if self.incise_divisions:
            numeric_map = self._make_division_incised_numeric_map(
                secondary_duration_pairs,
                prefix_talea,
                prefix_lengths,
                suffix_talea,
                suffix_lengths,
                prolation_addenda,
                )
        else:
            assert self.incise_output
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

    def _make_middle_of_numeric_map_part(self, middle):
        if self.fill_with_notes:
            if self.incise_divisions:
                if 0 < middle:
                    if self.body_ratio is not None:
                        shards = mathtools.divide_number_by_ratio(
                            middle, self.body_ratio)
                        return tuple(shards)
                    else:
                        return (middle,)
                else:
                    return ()
            elif self.incise_output:
                if 0 < middle:
                    return (middle,)
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)
        else:
            if self.incise_divisions:
                if 0 < middle:
                    return (-abs(middle),)
                else:
                    return ()
            elif self.incise_output:
                if 0 < middle:
                    return (-abs(middle), )
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)

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
                )
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _prepare_input(self, seeds):
        prefix_talea = self.prefix_talea or ()
        prefix_talea = \
            self.prefix_talea_helper(prefix_talea, seeds)
        prefix_lengths = self.prefix_lengths or ()
        prefix_lengths = \
            self.prefix_lengths_helper(prefix_lengths, seeds)
        suffix_talea = self.suffix_talea or ()
        suffix_talea = \
            self.suffix_talea_helper(suffix_talea, seeds)
        suffix_lengths = self.suffix_lengths or ()
        suffix_lengths = \
            self.suffix_lengths_helper(suffix_lengths, seeds)
        prolation_addenda = self.prolation_addenda or ()
        prolation_addenda = \
            self.prolation_addenda_helper(prolation_addenda, seeds)
        secondary_divisions = self.secondary_divisions or ()
        secondary_divisions = \
            self.secondary_divisions_helper(secondary_divisions, seeds)
        prefix_talea = datastructuretools.CyclicTuple(prefix_talea)
        suffix_talea = datastructuretools.CyclicTuple(suffix_talea)
        prefix_lengths = datastructuretools.CyclicTuple(prefix_lengths)
        suffix_lengths = datastructuretools.CyclicTuple(suffix_lengths)
        if prolation_addenda:
            prolation_addenda = datastructuretools.CyclicTuple(
                prolation_addenda)
        else:
            prolation_addenda = datastructuretools.CyclicTuple([0])
        secondary_divisions = datastructuretools.CyclicTuple(
            secondary_divisions)
        return (
            prefix_talea,
            prefix_lengths,
            suffix_talea,
            suffix_lengths,
            prolation_addenda,
            secondary_divisions,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def body_ratio(self):
        r'''Gets body ratio of rhythm-maker.

        ..  container:: example

            Sets `body_ratio` to divide middle part proportionally:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     prefix_talea=(-1,),
                ...     prefix_lengths=(0, 1),
                ...     suffix_talea=(-1,),
                ...     suffix_lengths=(1,),
                ...     talea_denominator=16,
                ...     body_ratio=(1, 1),
                ...     fill_with_notes=True,
                ...     incise_divisions=True,
                ...     )

            ::

                >>> divisions = 4 * [(5, 16)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns ratio.
        '''
        return self._body_ratio

    @property
    def fill_with_notes(self):
        r'''Gets fill with notes boolean.

        Returns boolean.
        '''
        return self._fill_with_notes

    @property
    def incise_divisions(self):
        r'''Gets incise divisions boolean.

        Returns boolean.
        '''
        return self._incise_divisions

    @property
    def incise_output(self):
        r'''Gets incise output boolean.

        ..  container:: example

            Output-incised notes:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     prefix_talea=(-8, -7),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(-3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     fill_with_notes=True,
                ...     incise_output=True,
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Output-incised rests:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     prefix_talea=(7, 8),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     fill_with_notes=False,
                ...     incise_output=True,
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns boolean.
        '''
        return self._incise_output

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses incised rhythm-maker.

        Returns newly constructed rhythm-maker.
        '''
        prefix_talea = self.prefix_talea
        if prefix_talea is not None:
            prefix_talea = tuple(reversed(prefix_talea))
        prefix_lengths = self.prefix_lengths
        if prefix_lengths is not None:
            prefix_lengths = tuple(reversed(prefix_lengths))
        suffix_talea = self.suffix_talea
        if suffix_talea is not None:
            suffix_talea = tuple(reversed(suffix_talea))
        suffix_lengths = self.suffix_lengths
        if suffix_lengths is not None:
            suffix_lengths = tuple(reversed(suffix_lengths))
        talea_denominator = self.talea_denominator
        body_ratio = self.body_ratio
        prolation_addenda = self.prolation_addenda
        if prolation_addenda is not None:
            prolation_addenda = tuple(reversed(prolation_addenda))
        secondary_divisions = self.secondary_divisions
        if secondary_divisions is not None:
            secondary_divisions = tuple(reversed(secondary_divisions))
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        fill_with_notes = self.fill_with_notes
        incise_divisions = self.incise_divisions
        incise_output = self.incise_output
        new = type(self)(
            prefix_talea=prefix_talea,
            prefix_lengths=prefix_lengths,
            suffix_talea=suffix_talea,
            suffix_lengths=suffix_lengths,
            talea_denominator=talea_denominator,
            body_ratio=body_ratio,
            prolation_addenda=prolation_addenda,
            secondary_divisions=secondary_divisions,
            decrease_durations_monotonically=decrease_durations_monotonically,
            fill_with_notes=fill_with_notes,
            incise_divisions=incise_divisions,
            incise_output=incise_output,
            )
        return new
