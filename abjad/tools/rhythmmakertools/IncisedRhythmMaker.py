# -*- encoding: utf-8 -*-
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach


class IncisedRhythmMaker(RhythmMaker):
    r'''Incised rhythm-maker.
    
    ..  container:: example

        ::

            >>> incise_specifier = rhythmmakertools.InciseSpecifier(
            ...     incise_divisions=True,
            ...     prefix_talea=(-1,),
            ...     prefix_lengths=(0, 1),
            ...     suffix_talea=(-1,),
            ...     suffix_lengths=(1,),
            ...     talea_denominator=16,
            ...     )
            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     incise_specifier=incise_specifier,
            ...     )

        ::

            >>> divisions = 4 * [(5, 16)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/16
                    c'4
                    r16
                }
                {
                    r16
                    c'8.
                    r16
                }
                {
                    c'4
                    r16
                }
                {
                    r16
                    c'8.
                    r16
                }
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_extra_counts_per_division',
        '_helper_functions',
        '_incise_specifier',
        '_split_divisions_by_counts',
        )

    _class_name_abbreviatio = 'In'

    _human_readable_class_name = 'incised rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        incise_specifier=None,
        split_divisions_by_counts=None,
        extra_counts_per_division=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        helper_functions=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            )
        prototype = (rhythmmakertools.InciseSpecifier, type(None))
        assert isinstance(incise_specifier, prototype)
        self._incise_specifier = incise_specifier
        extra_counts_per_division = \
            self._to_tuple(extra_counts_per_division)
        split_divisions_by_counts = \
            self._to_tuple(split_divisions_by_counts)
        assert extra_counts_per_division is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            extra_counts_per_division), extra_counts_per_division
        assert split_divisions_by_counts is None or \
            sequencetools.all_are_nonnegative_integer_equivalent_numbers(
            split_divisions_by_counts), split_divisions_by_counts
        self._extra_counts_per_division = extra_counts_per_division
        self._split_divisions_by_counts = split_divisions_by_counts
        if helper_functions is not None:
            assert isinstance(helper_functions, dict)
            for name in helper_functions:
                function = helper_functions.get(name)
                assert callable(function)
        self._helper_functions = helper_functions

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
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_division_incised_numeric_map(
        self, 
        duration_pairs=None,
        prefix_talea=None, 
        prefix_lengths=None,
        suffix_talea=None, 
        suffix_lengths=None, 
        extra_counts_per_division=None,
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
            prolation_addendum = extra_counts_per_division[pair_index]
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
        from abjad.tools import rhythmmakertools
        incise_specifier = self.incise_specifier
        if incise_specifier is None:
            incise_specifier = rhythmmakertools.InciseSpecifier()
        if incise_specifier.fill_with_notes:
            if incise_specifier.incise_divisions:
                if 0 < middle:
                    if incise_specifier.body_ratio is not None:
                        shards = mathtools.divide_number_by_ratio(
                            middle, incise_specifier.body_ratio)
                        return tuple(shards)
                    else:
                        return (middle,)
                else:
                    return ()
            elif incise_specifier.incise_output:
                if 0 < middle:
                    return (middle,)
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)
        else:
            if incise_specifier.incise_divisions:
                if 0 < middle:
                    return (-abs(middle),)
                else:
                    return ()
            elif incise_specifier.incise_output:
                if 0 < middle:
                    return (-abs(middle), )
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        input_ = self._prepare_input(seeds)
        prefix_talea = input_[0]
        prefix_lengths = input_[1]
        suffix_talea = input_[2]
        suffix_lengths = input_[3]
        extra_counts_per_division = input_[4]
        split_divisions_by_counts = input_[5]
        taleas = (
            prefix_talea, 
            suffix_talea, 
            extra_counts_per_division, 
            split_divisions_by_counts,
            )
        input_ = self._scale_taleas(
            duration_pairs, 
            self.incise_specifier.talea_denominator, 
            taleas,
            )
        duration_pairs = input_[0]
        lcd = input_[1]
        prefix_talea = input_[2]
        suffix_talea = input_[3]
        extra_counts_per_division = input_[4]
        split_divisions_by_counts = input_[5]
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, split_divisions_by_counts)
        incise_specifier = self.incise_specifier
        if incise_specifier is None:
            incise_specifier = rhythmmakertools.InciseSpecifier()
        if incise_specifier.incise_divisions:
            numeric_map = self._make_division_incised_numeric_map(
                secondary_duration_pairs,
                prefix_talea,
                prefix_lengths,
                suffix_talea,
                suffix_lengths,
                extra_counts_per_division,
                )
        else:
            assert incise_specifier.incise_output
            numeric_map = self._make_output_incised_numeric_map(
                secondary_duration_pairs,
                prefix_talea,
                prefix_lengths,
                suffix_talea,
                suffix_lengths,
                extra_counts_per_division,
                )
        result = []
        selections = \
            self._numeric_map_and_talea_denominator_to_leaf_selections(
            numeric_map, lcd)
        if not self.extra_counts_per_division:
            result.extend(selections)
        else:
            tuplets = self._make_tuplets(
                secondary_duration_pairs, 
                selections,
                )
            result.extend(tuplets)
        assert self._all_are_tuplets_or_all_are_leaf_selections(result)
        beam_specifier = self.beam_specifier
        if beam_specifier is None:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        if beam_specifier.beam_divisions_together:
            beam = spannertools.MultipartBeam()
            attach(beam, result)
        elif beam_specifier.beam_each_division:
            for x in result:
                beam = spannertools.MultipartBeam()
                attach(beam, x)
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
                suffix, 
                weights, 
                cyclic=False, 
                overhang=False,
                )[0]
        numeric_map_part = prefix + middle + suffix
        return numeric_map_part

    def _make_output_incised_numeric_map(
        self,
        duration_pairs,
        prefix_talea,
        prefix_lengths,
        suffix_talea,
        suffix_lengths,
        extra_counts_per_division,
        ):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        prefix_length, suffix_length = prefix_lengths[0], suffix_lengths[0]
        prefix = prefix_talea[
            prefix_talea_index:prefix_talea_index+prefix_length]
        suffix = suffix_talea[
            suffix_talea_index:suffix_talea_index+suffix_length]
        if len(duration_pairs) == 1:
            prolation_addendum = extra_counts_per_division[0]
            if isinstance(duration_pairs[0], mathtools.NonreducedFraction):
                numerator = duration_pairs[0].numerator
            else:
                numerator = duration_pairs[0][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        else:
            prolation_addendum = extra_counts_per_division[0]
            if isinstance(duration_pairs[0], tuple):
                numerator = duration_pairs[0][0]
            else:
                numerator = duration_pairs[0].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, ())
            numeric_map.append(numeric_map_part)
            for i, duration_pair in enumerate(duration_pairs[1:-1]):
                prolation_addendum = extra_counts_per_division[i+1]
                if isinstance(duration_pair, tuple):
                    numerator = duration_pair[0]
                else:
                    numerator = duration_pair.numerator
                numerator += (prolation_addendum % numerator)
                numeric_map_part = self._make_numeric_map_part(
                    numerator, (), ())
                numeric_map.append(numeric_map_part)
            try:
                prolation_addendum = extra_counts_per_division[i+2]
            except UnboundLocalError:
                prolation_addendum = extra_counts_per_division[1+2]
            if isinstance(duration_pairs[-1], tuple):
                numerator = duration_pairs[-1][0]
            else:
                numerator = duration_pairs[-1].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, (), suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map

    def _numeric_map_and_talea_denominator_to_leaf_selections(
        self, numeric_map, lcd):
        from abjad.tools import rhythmmakertools
        selections = []
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        for numeric_map_part in numeric_map:
            selection = scoretools.make_leaves_from_talea(
                numeric_map_part,
                lcd,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                )
            selections.append(selection)
        return selections

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

        extra_counts_per_division = self.extra_counts_per_division or ()
        helper = helper_functions.get('extra_counts_per_division')
        helper = self._none_to_trivial_helper(helper)
        extra_counts_per_division = helper(extra_counts_per_division, seeds)
        if extra_counts_per_division:
            extra_counts_per_division = datastructuretools.CyclicTuple(
                extra_counts_per_division)
        else:
            extra_counts_per_division = datastructuretools.CyclicTuple([0])

        split_divisions_by_counts = self.split_divisions_by_counts or ()
        helper = helper_functions.get('split_divisions_by_counts')
        helper = self._none_to_trivial_helper(helper)
        split_divisions_by_counts = helper(split_divisions_by_counts, seeds)
        split_divisions_by_counts = datastructuretools.CyclicTuple(
            split_divisions_by_counts)

        return (
            prefix_talea,
            prefix_lengths,
            suffix_talea,
            suffix_lengths,
            extra_counts_per_division,
            split_divisions_by_counts,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def helper_functions(self):
        r'''Gets helper functions of incised rhythm-maker.

        Returns dictionary or none.
        '''
        return self._helper_functions

    @property
    def incise_specifier(self):
        r'''Gets incise specifier or incised rhythm-maker.

        ..  container:: example

            Output-incised notes:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     incise_output=True,
                ...     prefix_talea=(-8, -7),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(-3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        r4
                        r8..
                        c'8 [ ~
                        c'32 ]
                    }
                    {
                        c'2 ~
                        c'8
                    }
                    {
                        c'4
                        r16.
                        r16.
                        r16.
                        r16.
                    }
                }

        ..  container:: example

            Output-incised rests:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     incise_output=True,
                ...     prefix_talea=(7, 8),
                ...     prefix_lengths=(2,),
                ...     suffix_talea=(3,),
                ...     suffix_lengths=(4,),
                ...     talea_denominator=32,
                ...     fill_with_notes=False,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (5, 8), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'8..
                        c'4
                        r8
                        r32
                    }
                    {
                        r2
                        r8
                    }
                    {
                        r4
                        c'16. [
                        c'16.
                        c'16.
                        c'16. ]
                    }
                }

        Returns incise specifier or none.
        '''
        return self._incise_specifier

    @property
    def extra_counts_per_division(self):
        r'''Gets prolation addenda of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._extra_counts_per_division

    @property
    def split_divisions_by_counts(self):
        r'''Gets secondary divisions of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._split_divisions_by_counts

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses incised rhythm-maker.

        Returns newly constructed rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        extra_counts_per_division = self.extra_counts_per_division
        if extra_counts_per_division is not None:
            extra_counts_per_division = tuple(reversed(extra_counts_per_division))
        split_divisions_by_counts = self.split_divisions_by_counts
        if split_divisions_by_counts is not None:
            split_divisions_by_counts = tuple(reversed(split_divisions_by_counts))
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        specifier = specifier.reverse()
        maker = new(
            self,
            extra_counts_per_division=extra_counts_per_division,
            split_divisions_by_counts=split_divisions_by_counts,
            duration_spelling_specifier=specifier,
            )
        return maker
