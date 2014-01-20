# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class IncisedRhythmMaker(RhythmMaker):
    r'''Incised rhythm-maker.
    
    Rhythm makers can incise the edge of every output cell.

    Or rhythm-makers can incise only the start of the first output cell
    and the end of the last output cell.


    ..  container:: example

        Division-incised notes:

        ::

            >>> incise_specifier = rhythmmakertools.InciseSpecifier(
            ...     prefix_talea=(-1,),
            ...     prefix_lengths=(0, 1),
            ...     suffix_talea=(-1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=16,
            ...     )
            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     incise_specifier=incise_specifier,
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

    ### CLASS VARIABLES ###

    __slots__ = (
        '_body_ratio',
        '_fill_with_notes',
        '_helper_functions',
        '_incise_output',
        '_incise_divisions',
        '_incise_specifier',
        '_prolation_addenda',
        '_secondary_divisions',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        incise_specifier=None,
        body_ratio=None,
        prolation_addenda=None,
        secondary_divisions=None,
        helper_functions=None,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        beam_each_cell=False,
        beam_cells_together=False,
        fill_with_notes=True,
        incise_divisions=False,
        incise_output=False,
        tie_across_divisions=False,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_cells_together=beam_cells_together,
            beam_each_cell=beam_each_cell,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_across_divisions=tie_across_divisions,
            )
        incise_specifier = incise_specifier or \
            rhythmmakertools.InciseSpecifier()
        self._incise_specifier = incise_specifier
        prolation_addenda = \
            self._to_tuple(prolation_addenda)
        secondary_divisions = \
            self._to_tuple(secondary_divisions)

        if helper_functions is not None:
            assert isinstance(helper_functions, dict)
            for name in helper_functions:
                function = helper_functions.get(name)
                assert callable(function)
        self._helper_functions = helper_functions
        assert prolation_addenda is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            prolation_addenda), prolation_addenda
        assert secondary_divisions is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            secondary_divisions), secondary_divisions
        self._prolation_addenda = prolation_addenda
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self._body_ratio = body_ratio
        self._secondary_divisions = secondary_divisions
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
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __makenew__(self, *args, **kwargs):
        r'''Makes new incised rhythm-maker with optional `kwargs`.

        Returns new incised rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'forbidden_written_duration': self.forbidden_written_duration,
            'incise_specifier': self.incise_specifier,
            'body_ratio': self.body_ratio,
            'prolation_addenda': self.prolation_addenda,
            'secondary_divisions': self.secondary_divisions,
            'helper_functions': self.helper_functions,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'fill_with_notes': self.fill_with_notes,
            'incise_divisions': self.incise_divisions,
            'incise_output': self.incise_output,
            }
        arguments.update(kwargs)
        maker = type(self)(**arguments)
        return maker

    ### PRIVATE METHODS ###

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

    def _make_music(self, duration_pairs, seeds):
        result = self._prepare_input(seeds)
        prefix_talea, prefix_lengths, suffix_talea, suffix_lengths = \
            result[:-2]
        prolation_addenda, secondary_divisions = result[-2:]
        taleas = (
            prefix_talea, 
            suffix_talea, 
            prolation_addenda, 
            secondary_divisions,
            )
        result = self._scale_taleas(
            duration_pairs, 
            self.incise_specifier.talea_denominator, 
            taleas,
            )
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
        helper_functions = self.helper_functions or {}
        prefix_talea = self.incise_specifier.prefix_talea or ()
        helper = helper_functions.get('prefix_talea')
        helper = self._none_to_trivial_helper(helper)
        prefix_talea = helper(prefix_talea, seeds)
        prefix_talea = datastructuretools.CyclicTuple(prefix_talea)

        prefix_lengths = self.incise_specifier.prefix_lengths or ()
        helper = helper_functions.get('prefix_lengths')
        helper = self._none_to_trivial_helper(helper)
        prefix_lengths = helper(prefix_lengths, seeds)
        prefix_lengths = datastructuretools.CyclicTuple(prefix_lengths)

        suffix_talea = self.incise_specifier.suffix_talea or ()
        helper = helper_functions.get('suffix_talea')
        helper = self._none_to_trivial_helper(helper)
        suffix_talea = helper(suffix_talea, seeds)
        suffix_talea = datastructuretools.CyclicTuple(suffix_talea)

        suffix_lengths = self.incise_specifier.suffix_lengths or ()
        helper = helper_functions.get('suffix_lengths')
        helper = self._none_to_trivial_helper(helper)
        suffix_lengths = helper(suffix_lengths, seeds)
        suffix_lengths = datastructuretools.CyclicTuple(suffix_lengths)

        prolation_addenda = self.prolation_addenda or ()
        helper = helper_functions.get('prolation_addenda')
        helper = self._none_to_trivial_helper(helper)
        prolation_addenda = helper(prolation_addenda, seeds)
        if prolation_addenda:
            prolation_addenda = datastructuretools.CyclicTuple(
                prolation_addenda)
        else:
            prolation_addenda = datastructuretools.CyclicTuple([0])

        secondary_divisions = self.secondary_divisions or ()
        helper = helper_functions.get('secondary_divisions')
        helper = self._none_to_trivial_helper(helper)
        secondary_divisions = helper(secondary_divisions, seeds)
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

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=(-1,),
                ...     prefix_lengths=(0, 1),
                ...     suffix_talea=(-1,),
                ...     suffix_lengths=(1,),
                ...     talea_denominator=16,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
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
    def helper_functions(self):
        r'''Gets helper functions of incised rhythm-maker.

        Returns dictionary or none.
        '''
        return self._helper_functions

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

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=(-8, -7),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(-3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
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

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=(7, 8),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
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

    @property
    def incise_specifier(self):
        r'''Gets incision specifier or incised rhythm-maker.

        Returns incision specifier.
        '''
        return self._incise_specifier

    @property
    def prolation_addenda(self):
        r'''Gets prolation addenda of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._prolation_addenda

    @property
    def secondary_divisions(self):
        r'''Gets secondary divisions of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._secondary_divisions

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses incised rhythm-maker.

        Returns newly constructed rhythm-maker.
        '''
        prolation_addenda = self.prolation_addenda
        if prolation_addenda is not None:
            prolation_addenda = tuple(reversed(prolation_addenda))
        secondary_divisions = self.secondary_divisions
        if secondary_divisions is not None:
            secondary_divisions = tuple(reversed(secondary_divisions))
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        maker = new(
            self,
            decrease_durations_monotonically=decrease_durations_monotonically,
            prolation_addenda=prolation_addenda,
            secondary_divisions=secondary_divisions,
            )
        return maker
