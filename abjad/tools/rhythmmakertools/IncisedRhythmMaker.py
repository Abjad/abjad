# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import new


class IncisedRhythmMaker(RhythmMaker):
    r'''Incised rhythm-maker.

    ..  container:: example

        ::

            >>> maker = rhythmmakertools.IncisedRhythmMaker(
            ...     incise_specifier=rhythmmakertools.InciseSpecifier(
            ...         prefix_talea=[-1],
            ...         prefix_counts=[0, 1],
            ...         suffix_talea=[-1],
            ...         suffix_counts=[1],
            ...         talea_denominator=16,
            ...         ),
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

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_extra_counts_per_division',
        '_helper_functions',
        '_incise_specifier',
        '_split_divisions_by_counts',
        )

    _class_name_abbreviation = 'In'

    _human_readable_class_name = 'incised rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        incise_specifier=None,
        split_divisions_by_counts=None,
        extra_counts_per_division=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        output_masks=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        helper_functions=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            output_masks=output_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        prototype = (rhythmmakertools.InciseSpecifier, type(None))
        assert isinstance(incise_specifier, prototype)
        self._incise_specifier = incise_specifier
        extra_counts_per_division = \
            self._to_tuple(extra_counts_per_division)
        split_divisions_by_counts = \
            self._to_tuple(split_divisions_by_counts)
        assert extra_counts_per_division is None or \
            mathtools.all_are_nonnegative_integer_equivalent_numbers(
            extra_counts_per_division), extra_counts_per_division
        assert split_divisions_by_counts is None or \
            mathtools.all_are_nonnegative_integer_equivalent_numbers(
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

    def __call__(self, divisions, rotation=None):
        r'''Calls incised rhythm-maker on `divisions`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    ### PRIVATE METHODS ###

    def _get_incise_specifier(self):
        from abjad.tools import rhythmmakertools
        if self.incise_specifier is not None:
            return self.incise_specifier
        return rhythmmakertools.InciseSpecifier()

    def _make_division_incised_numeric_map(
        self,
        divisions=None,
        prefix_talea=None,
        prefix_counts=None,
        suffix_talea=None,
        suffix_counts=None,
        extra_counts_per_division=None,
        ):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        for pair_index, division in enumerate(divisions):
            prefix_length, suffix_length = \
                prefix_counts[pair_index], suffix_counts[pair_index]
            prefix = prefix_talea[
                prefix_talea_index:prefix_talea_index+prefix_length]
            suffix = suffix_talea[
                suffix_talea_index:suffix_talea_index+suffix_length]
            prefix_talea_index += prefix_length
            suffix_talea_index += suffix_length
            prolation_addendum = extra_counts_per_division[pair_index]
            if isinstance(division, tuple):
                numerator = division[0] + (
                    prolation_addendum % division[0])
            else:
                numerator = division.numerator + (
                    prolation_addendum % division.numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map

    def _make_middle_of_numeric_map_part(self, middle):
        incise_specifier = self._get_incise_specifier()
        if incise_specifier.fill_with_notes:
            if not incise_specifier.outer_divisions_only:
                if 0 < middle:
                    if incise_specifier.body_ratio is not None:
                        shards = mathtools.divide_number_by_ratio(
                            middle, incise_specifier.body_ratio)
                        return tuple(shards)
                    else:
                        return (middle,)
                else:
                    return ()
            elif incise_specifier.outer_divisions_only:
                if 0 < middle:
                    return (middle,)
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)
        else:
            if not incise_specifier.outer_divisions_only:
                if 0 < middle:
                    return (-abs(middle),)
                else:
                    return ()
            elif incise_specifier.outer_divisions_only:
                if 0 < middle:
                    return (-abs(middle),)
                else:
                    return ()
            else:
                message = 'must incise divisions or output.'
                raise Exception(message)

    def _make_music(self, divisions, rotation):
        from abjad.tools import rhythmmakertools
        input_divisions = divisions[:]
        input_ = self._prepare_input(rotation)
        prefix_talea = input_[0]
        prefix_counts = input_[1]
        suffix_talea = input_[2]
        suffix_counts = input_[3]
        extra_counts_per_division = input_[4]
        split_divisions_by_counts = input_[5]
        taleas = (
            prefix_talea,
            suffix_talea,
            extra_counts_per_division,
            split_divisions_by_counts,
            )
        if self.incise_specifier is not None:
            talea_denominator = self.incise_specifier.talea_denominator
        else:
            talea_denominator = None
        input_ = self._scale_taleas(
            divisions,
            talea_denominator,
            taleas,
            )
        divisions = input_[0]
        lcd = input_[1]
        prefix_talea = input_[2]
        suffix_talea = input_[3]
        extra_counts_per_division = input_[4]
        split_divisions_by_counts = input_[5]
        secondary_divisions = self._make_secondary_divisions(
            divisions, split_divisions_by_counts)
        incise_specifier = self._get_incise_specifier()
        if not incise_specifier.outer_divisions_only:
            numeric_map = self._make_division_incised_numeric_map(
                secondary_divisions,
                prefix_talea,
                prefix_counts,
                suffix_talea,
                suffix_counts,
                extra_counts_per_division,
                )
        else:
            assert incise_specifier.outer_divisions_only
            numeric_map = self._make_output_incised_numeric_map(
                secondary_divisions,
                prefix_talea,
                prefix_counts,
                suffix_talea,
                suffix_counts,
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
                secondary_divisions,
                selections,
                )
            result.extend(tuplets)
        assert self._all_are_tuplets_or_all_are_leaf_selections(result)
        beam_specifier = self._get_beam_specifier()
        if beam_specifier.beam_divisions_together:
            beam = spannertools.MultipartBeam()
            attach(beam, result)
        elif beam_specifier.beam_each_division:
            for x in result:
                beam = spannertools.MultipartBeam()
                attach(beam, x)
        selections = [selectiontools.Selection(x) for x in result]
        selections = self._apply_output_masks(selections, rotation)
        duration_specifier = self._get_duration_spelling_specifier()
        if duration_specifier.rewrite_meter:
            selections = duration_specifier._rewrite_meter_(
                selections,
                input_divisions,
                )
        return selections

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
            prefix = sequencetools.split_sequence(
                prefix, weights, cyclic=False, overhang=False)[0]
        middle = self._make_middle_of_numeric_map_part(middle)
        suffix_space = numerator - prefix_weight
        if suffix_space <= 0:
            suffix = ()
        elif suffix_space < suffix_weight:
            weights = [suffix_space]
            suffix = sequencetools.split_sequence(
                suffix,
                weights,
                cyclic=False,
                overhang=False,
                )[0]
        numeric_map_part = prefix + middle + suffix
        return [durationtools.Duration(x) for x in numeric_map_part]

    def _make_output_incised_numeric_map(
        self,
        divisions,
        prefix_talea,
        prefix_counts,
        suffix_talea,
        suffix_counts,
        extra_counts_per_division,
        ):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        prefix_length, suffix_length = prefix_counts[0], suffix_counts[0]
        prefix = prefix_talea[
            prefix_talea_index:prefix_talea_index+prefix_length]
        suffix = suffix_talea[
            suffix_talea_index:suffix_talea_index+suffix_length]
        if len(divisions) == 1:
            prolation_addendum = extra_counts_per_division[0]
            if isinstance(divisions[0], mathtools.NonreducedFraction):
                numerator = divisions[0].numerator
            else:
                numerator = divisions[0][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        else:
            prolation_addendum = extra_counts_per_division[0]
            if isinstance(divisions[0], tuple):
                numerator = divisions[0][0]
            else:
                numerator = divisions[0].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, prefix, ())
            numeric_map.append(numeric_map_part)
            for i, division in enumerate(divisions[1:-1]):
                prolation_addendum = extra_counts_per_division[i+1]
                if isinstance(division, tuple):
                    numerator = division[0]
                else:
                    numerator = division.numerator
                numerator += (prolation_addendum % numerator)
                numeric_map_part = self._make_numeric_map_part(
                    numerator, (), ())
                numeric_map.append(numeric_map_part)
            try:
                prolation_addendum = extra_counts_per_division[i+2]
            except UnboundLocalError:
                prolation_addendum = extra_counts_per_division[1+2]
            if isinstance(divisions[-1], tuple):
                numerator = divisions[-1][0]
            else:
                numerator = divisions[-1].numerator
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(
                numerator, (), suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map

    def _numeric_map_and_talea_denominator_to_leaf_selections(
        self, numeric_map, lcd):
        from abjad.tools import rhythmmakertools
        selections = []
        specifier = self._get_duration_spelling_specifier()
        tie_specifier = self._get_tie_specifier()
        for numeric_map_part in numeric_map:
            numeric_map_part = [
                _ for _ in numeric_map_part if _ != durationtools.Duration(0)
                ]
            selection = scoretools.make_leaves_from_talea(
                numeric_map_part,
                lcd,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                spell_metrically=specifier.spell_metrically,
                use_messiaen_style_ties=tie_specifier.use_messiaen_style_ties,
                )
            selections.append(selection)
        return selections

    def _prepare_input(self, rotation):
        from abjad.tools import rhythmmakertools
        helper_functions = self.helper_functions or {}
        incise_specifier = self._get_incise_specifier()
        prefix_talea = incise_specifier.prefix_talea or ()
        helper = helper_functions.get('prefix_talea')
        helper = self._none_to_trivial_helper(helper)
        prefix_talea = helper(prefix_talea, rotation)
        prefix_talea = datastructuretools.CyclicTuple(prefix_talea)

        prefix_counts = incise_specifier.prefix_counts or (0,)
        helper = helper_functions.get('prefix_counts')
        helper = self._none_to_trivial_helper(helper)
        prefix_counts = helper(prefix_counts, rotation)
        prefix_counts = datastructuretools.CyclicTuple(prefix_counts)

        suffix_talea = incise_specifier.suffix_talea or ()
        helper = helper_functions.get('suffix_talea')
        helper = self._none_to_trivial_helper(helper)
        suffix_talea = helper(suffix_talea, rotation)
        suffix_talea = datastructuretools.CyclicTuple(suffix_talea)

        suffix_counts = incise_specifier.suffix_counts or (0,)
        helper = helper_functions.get('suffix_counts')
        helper = self._none_to_trivial_helper(helper)
        suffix_counts = helper(suffix_counts, rotation)
        suffix_counts = datastructuretools.CyclicTuple(suffix_counts)

        extra_counts_per_division = self.extra_counts_per_division or ()
        helper = helper_functions.get('extra_counts_per_division')
        helper = self._none_to_trivial_helper(helper)
        extra_counts_per_division = helper(extra_counts_per_division, rotation)
        if extra_counts_per_division:
            extra_counts_per_division = datastructuretools.CyclicTuple(
                extra_counts_per_division)
        else:
            extra_counts_per_division = datastructuretools.CyclicTuple([0])

        split_divisions_by_counts = self.split_divisions_by_counts or ()
        helper = helper_functions.get('split_divisions_by_counts')
        helper = self._none_to_trivial_helper(helper)
        split_divisions_by_counts = helper(split_divisions_by_counts, rotation)
        split_divisions_by_counts = datastructuretools.CyclicTuple(
            split_divisions_by_counts)

        return (
            prefix_talea,
            prefix_counts,
            suffix_talea,
            suffix_counts,
            extra_counts_per_division,
            split_divisions_by_counts,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of incised rhythm-maker.

        ..  container:: example

            **Example 1.** Spells durations with the fewest number of glyphs:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'2 ~
                        c'8
                        r8
                    }
                }

        ..  container:: example

            **Example 2.** Forbids notes with written duration greater than or
            equal to ``1/2``:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         forbidden_written_duration=Duration(1, 2),
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'4 ~
                        c'4 ~
                        c'4.
                    }
                    {
                        \time 4/8
                        c'4 ~
                        c'4
                    }
                    {
                        \time 6/8
                        c'4 ~
                        c'4 ~
                        c'8
                        r8
                    }
                }

        ..  container:: example

            **Example 3a.** Spells all divisions metrically when
            `spell_metrically` is true:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'4. ~
                        c'4 ~
                        c'4
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'4. ~
                        c'4
                        r8
                    }
                }

            **Example 3b.** Spells only unassignable durations metrically when
            `spell_metrically` is ``'unassignable'``:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'4. ~
                        c'4
                        r8
                    }
                }

            **Example 3c.** Rewrites meter:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         rewrite_meter=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'4. ~
                        c'4
                        r8
                    }
                }

        Returns duration spelling specifier or none.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.duration_spelling_specifier

    @property
    def extra_counts_per_division(self):
        r'''Gets prolation addenda of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._extra_counts_per_division

    @property
    def helper_functions(self):
        r'''Gets helper functions of incised rhythm-maker.

        Returns dictionary or none.
        '''
        return self._helper_functions

    @property
    def incise_specifier(self):
        r'''Gets incise specifier of incised rhythm-maker.

        ..  container:: example

            **Example 1.** Doesn't incise:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker()

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
                        c'2 ~
                        c'8
                    }
                    {
                        c'2 ~
                        c'8
                    }
                    {
                        c'2 ~
                        c'8
                    }
                }

        ..  container:: example

            **Example 2.** Fills divisions with notes. 
            Incises outer divisions only:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-8, -7],
                ...     prefix_counts=[2],
                ...     suffix_talea=[-3],
                ...     suffix_counts=[4],
                ...     talea_denominator=32,
                ...     outer_divisions_only=True,
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
                        c'8 ~ [
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

            **Example 3.** Fills divisions with rests. Incises outer divisions
            only:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[7, 8],
                ...     prefix_counts=[2],
                ...     suffix_talea=[3],
                ...     suffix_counts=[4],
                ...     talea_denominator=32,
                ...     fill_with_notes=False,
                ...     outer_divisions_only=True,
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
    def output_masks(self):
        r'''Gets output masks of incised rhythm-maker.

        ..  container:: example

            **Example 1.** No output masks:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         talea_denominator=16,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
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
                        \time 4/8
                        r16
                        c'4..
                    }
                    {
                        \time 3/8
                        r16
                        c'4 ~
                        c'16
                    }
                    {
                        \time 4/8
                        r16
                        c'4..
                    }
                    {
                        \time 3/8
                        r16
                        c'4 ~
                        c'16
                    }
                }

        ..  container:: example

            **Example 2.** Masks every other output division:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         talea_denominator=16,
                ...         ),
                ...     output_masks=[
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             period=2,
                ...             ),
                ...         ],
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
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
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r16
                        c'4 ~
                        c'16
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r16
                        c'4 ~
                        c'16
                    }
                }

        Set to output masks or none.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.output_masks

    @property
    def split_divisions_by_counts(self):
        r'''Gets secondary divisions of incised rhythm-maker.

        Returns tuple or none.
        '''
        return self._split_divisions_by_counts

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of incised rhythm-maker.

        ..  container:: example

            **Example 1.** Does not tie across divisions:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'2 ~
                        c'8
                        r8
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Ties across divisions:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2.. ~
                    }
                    {
                        \time 4/8
                        c'2 ~
                    }
                    {
                        \time 6/8
                        c'2 ~
                        c'8
                        r8
                    }
                }

        ..  container:: example

            **Example 3.** Patterns ties across divisions:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0],
                ...     period=2,
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2.. ~
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'2 ~
                        c'8
                        r8
                    }
                }

        ..  container:: example

            **Example 4.** Uses Messiaen-style ties:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2 \repeatTie
                    }
                    {
                        \time 6/8
                        c'2 \repeatTie
                        c'8 \repeatTie
                        r8
                    }
                }

        ..  container:: example

            **Example 5.** Strips all ties:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         strip_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'2..
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'2
                        c'8
                        r8
                    }
                }

        ..  container:: example

            **Example 6.** Spells durations metrically and then strips all
            ties:

            ::

                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     incise_specifier=rhythmmakertools.InciseSpecifier(
                ...         prefix_talea=[-1],
                ...         prefix_counts=[1],
                ...         outer_divisions_only=True,
                ...         suffix_talea=[-1],
                ...         suffix_counts=[1],
                ...         talea_denominator=8,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         strip_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(8, 8), (4, 8), (6, 8)]
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
                        \time 8/8
                        r8
                        c'4.
                        c'4
                        c'4
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 6/8
                        c'4.
                        c'4
                        r8
                    }
                }

        Defaults to none.

        Set to tie specifier or none.

        Returns tie specifier or none.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of incised rhythm-maker.

        ..  note:: not yet implemented.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(IncisedRhythmMaker, self)
        return superclass.tuplet_spelling_specifier