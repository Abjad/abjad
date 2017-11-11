import math
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools.topleveltools import inspect
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class EvenDivisionRhythmMaker(RhythmMaker):
    r'''Even division rhythm-maker.

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a list of selections as
    output (structured one selection per input division).
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_burnish_specifier',
        '_denominators',
        '_extra_counts_per_division',
        '_preferred_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        denominators=[8],
        beam_specifier=None,
        burnish_specifier=None,
        logical_tie_masks=None,
        division_masks=None,
        duration_specifier=None,
        extra_counts_per_division=None,
        preferred_denominator='from_counts',
        tie_specifier=None,
        tuplet_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            logical_tie_masks=logical_tie_masks,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        assert mathtools.all_are_nonnegative_integer_powers_of_two(
            denominators), repr(denominators)
        denominators = tuple(denominators)
        self._denominators = denominators
        if extra_counts_per_division is not None:
            assert mathtools.all_are_integer_equivalent(
                extra_counts_per_division), repr(extra_counts_per_division)
            extra_counts_per_division = [
                int(_) for _ in extra_counts_per_division
                ]
            extra_counts_per_division = tuple(extra_counts_per_division)
        self._extra_counts_per_division = extra_counts_per_division
        prototype = (rhythmmakertools.BurnishSpecifier, type(None))
        assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier
        extra_counts_per_division = extra_counts_per_division or (0,)
        self._preferred_denominator = preferred_denominator

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls even division rhythm-maker on `divisions`.

        ..  container:: example

            Fills divisions with alternating eighth and sixteenth notes:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[8, 16],
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            Adds extra counts per division according to a pattern of three
            elements:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[0, 1, 2],
            ...     )

            >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/8 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        Returns list of of selections.
        '''
        superclass = super(EvenDivisionRhythmMaker, self)
        return superclass.__call__(
            divisions,
            rotation=rotation,
            )

    ### PRIVATE METHODS ###

    def _apply_burnish_specifier(self, selections, rotation):
        import abjad
        if self.burnish_specifier is None:
            return selections
        left_classes = self.burnish_specifier.left_classes
        middle_classes = self.burnish_specifier.middle_classes
        right_classes = self.burnish_specifier.right_classes
        left_counts = self.burnish_specifier.left_counts
        right_counts = self.burnish_specifier.right_counts
        left_classes = left_classes or ()
        left_classes = abjad.sequence(left_classes).rotate(n=rotation)
        left_classes = abjad.CyclicTuple(left_classes)
        if middle_classes == () or middle_classes is None:
            middle_classes = (0,)
        middle_classes = abjad.sequence(middle_classes).rotate(n=rotation)
        middle_classes = abjad.CyclicTuple(middle_classes)
        right_classes = right_classes or ()
        right_classes = abjad.sequence(right_classes).rotate(n=rotation)
        right_classes = abjad.CyclicTuple(right_classes)
        left_counts = left_counts or (0,)
        left_counts = abjad.sequence(left_counts).rotate(n=rotation)
        left_counts = abjad.CyclicTuple(left_counts)
        right_counts = right_counts or (0,)
        right_counts = abjad.sequence(right_counts).rotate(n=rotation)
        right_counts = abjad.CyclicTuple(right_counts)
        if self.burnish_specifier.outer_divisions_only:
            procedure = self._burnish_outer_selections
        else:
            procedure = self._burnish_each_selection
        selections = procedure(
            selections,
            left_classes,
            middle_classes,
            right_classes,
            left_counts,
            right_counts,
            )
        return selections

    def _burnish_division_part(self, division_part, token):
        import abjad
        assert len(division_part) == len(token)
        new_division_part = []
        for leaf, burnishing in zip(division_part, token):
            if burnishing in (-1, abjad.Rest):
                new_division_part.append(abjad.Rest(leaf))
            elif burnishing == 0:
                new_division_part.append(leaf)
            elif burnishing in (1, abjad.Note):
                new_division_part.append(abjad.Note(leaf))
            else:
                message = 'unknown burnishing: {!r}.'
                message = message.format(burnishing)
                raise ValueError(message)
        new_division_part = type(division_part)(new_division_part)
        return new_division_part

    def _burnish_each_selection(
        self,
        selections,
        left_classes,
        middle_classes,
        right_classes,
        left_counts,
        right_counts,
        ):
        import abjad
        lefts_index, rights_index = 0, 0
        for selection_index, selection in enumerate(selections):
            tuplet = selection[0]
            original_duration = inspect(tuplet).get_duration()
            leaves = tuplet[:]
            leaf_count = len(leaves)
            left_length = left_counts[selection_index]
            left = left_classes[lefts_index:lefts_index + left_length]
            lefts_index += left_length
            right_length = right_counts[selection_index]
            right = right_classes[rights_index:rights_index + right_length]
            rights_index += right_length
            available_left_length = leaf_count
            left_length = min([left_length, available_left_length])
            available_right_length = leaf_count - left_length
            right_length = min([right_length, available_right_length])
            middle_length = leaf_count - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middle_classes[selection_index]]
            right = right[:right_length]
            result = abjad.sequence(leaves).partition_by_counts(
                [left_length, middle_length, right_length],
                cyclic=False,
                overhang=False,
                )
            left_part, middle_part, right_part = result
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_leaves = left_part + middle_part + right_part
            tuplet[:] = burnished_leaves
            assert inspect(tuplet).get_duration() == original_duration
        return selections

    def _burnish_outer_selections(
        self,
        selections,
        left_classes,
        middle_classes,
        right_classes,
        left_counts,
        right_counts,
        ):
        import abjad
        if len(selections) == 1:
            self._burnish_each_selection(
                selections,
                left_classes,
                middle_classes,
                right_classes,
                left_counts,
                right_counts,
                )
            return selections
        left_length = 0
        if left_counts:
            left_length = left_counts[0]
        left = left_classes[:left_length]
        right_length = 0
        if right_counts:
            right_length = right_counts[0]
        right = right_classes[:right_length]

        # first selection
        tuplet = selections[0][0]
        original_duration = inspect(tuplet).get_duration()
        leaves = tuplet[:]
        available_left_length = len(leaves)
        left_length = min([left_length, available_left_length])
        middle_length = len(leaves) - left_length
        left = left[:left_length]
        if not middle_classes:
            middle_classes = [1]
        middle = [middle_classes[0]]
        middle = middle_length * middle
        left_part, middle_part = abjad.sequence(leaves).partition_by_counts(
            [left_length, middle_length],
            cyclic=False,
            overhang=False,
            )
        left_part = self._burnish_division_part(left_part, left)
        middle_part = self._burnish_division_part(middle_part, middle)
        burnished_leaves = left_part + middle_part
        tuplet[:] = burnished_leaves
        assert inspect(tuplet).get_duration() == original_duration

        # middle selections
        for selection in selections[1:-1]:
            tuplet = selection[0]
            original_duration = inspect(tuplet).get_duration()
            leaves = tuplet[:]
            middle = len(leaves) * [middle_classes[0]]
            burnished_leaves = self._burnish_division_part(leaves, middle)
            tuplet[:] = burnished_leaves
            assert inspect(tuplet).get_duration() == original_duration

        # last selection
        tuplet = selections[-1][0]
        original_duration = inspect(tuplet).get_duration()
        leaves = tuplet[:]
        available_right_length = len(leaves)
        right_length = min([right_length, available_right_length])
        middle_length = len(leaves) - right_length
        right = right[:right_length]
        middle = middle_length * [middle_classes[0]]
        middle_part, right_part = abjad.sequence(leaves).partition_by_counts(
            [middle_length, right_length],
            cyclic=False,
            overhang=False,
            )
        middle_part = self._burnish_division_part(middle_part, middle)
        right_part = self._burnish_division_part(right_part, right)
        burnished_leaves = middle_part + right_part
        tuplet[:] = burnished_leaves
        assert inspect(tuplet).get_duration() == original_duration
        return selections

    def _make_music(self, divisions, rotation):
        import abjad
        if rotation is None:
            rotation = 0
        selections = []
        divisions = [abjad.NonreducedFraction(_) for _ in divisions]
        denominators = abjad.CyclicTuple(self.denominators)
        extra_counts_per_division = self.extra_counts_per_division or (0,)
        extra_counts_per_division = abjad.CyclicTuple(
            extra_counts_per_division
            )
        for i, division in enumerate(divisions, rotation):
            # not yet extended to work with non-power-of-two divisions
            if not abjad.mathtools.is_positive_integer_power_of_two(
                division.denominator):
                message = 'non-power-of-two divisions not implemented: {!r}.'
                message = message.format(division)
                raise Exception(message)
            denominator = denominators[i]
            extra_count = extra_counts_per_division[i]
            basic_duration = abjad.Duration(1, denominator)
            unprolated_note_count = None
            maker = abjad.NoteMaker()
            if division < 2 * basic_duration:
                notes = maker([0], [division])
            else:
                unprolated_note_count = division / basic_duration
                unprolated_note_count = int(unprolated_note_count)
                unprolated_note_count = unprolated_note_count or 1
                if 0 < extra_count:
                    modulus = unprolated_note_count
                    extra_count = extra_count % modulus
                elif extra_count < 0:
                    modulus = int(math.ceil(unprolated_note_count / 2.0))
                    extra_count = abs(extra_count) % modulus
                    extra_count *= -1
                note_count = unprolated_note_count + extra_count
                durations = note_count * [basic_duration]
                notes = maker([0], durations)
                assert all(
                    _.written_duration.denominator == denominator
                    for _ in notes
                    )
            tuplet_duration = abjad.Duration(division)
            tuplet = abjad.Tuplet.from_duration(tuplet_duration, notes)
            if (self.preferred_denominator == 'from_counts' and
                unprolated_note_count is not None):
                preferred_denominator = unprolated_note_count
                tuplet.preferred_denominator = preferred_denominator
            elif isinstance(self.preferred_denominator, int):
                tuplet.preferred_denominator = self.preferred_denominator
            selection = abjad.Selection(tuplet)
            selections.append(selection)
        selections = self._apply_burnish_specifier(selections, rotation)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        selections = self._apply_division_masks(selections, rotation)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier.

        ..  container:: example

            Forces the first leaf and the last two leaves to be rests:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         right_classes=[abjad.Rest],
            ...         right_counts=[2],
            ...         outer_divisions_only=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/8
                        {
                            r8
                            c'8 [
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8 ]
                            r8
                            r8
                        }
                    } % measure
                }

            Burnishing outer divisions also works when given a single division:

            >>> divisions = [(7, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        {
                            r8
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                            r8
                            r8
                        }
                    } % measure
                }

        ..  container:: example

            Forces the first leaf of every division to be a rest:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         ),
            ...     )

            >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/8
                        {
                            r8
                            c'8 [
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            r8
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            r8
                            c'8 [
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            r8
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        Returns burnish specifier or none.
        '''
        return self._burnish_specifier

    @property
    def denominators(self):
        r'''Gets denominators.

        ..  container:: example

            Fills divisions with 16th notes:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     )

            >>> divisions = [(3, 16), (3, 8), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/16
                        {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/4
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Fills divisions with 8th notes:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[8],
            ...     )

            >>> divisions = [(3, 16), (3, 8), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/16
                        {
                            c'8.
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/4
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

            Fills divisions less than twice the duration of an eighth note with
            a single attack.

        ..  container:: example

            Fills divisions with quarter notes:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[4],
            ...     )

            >>> divisions = [(3, 16), (3, 8), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/16
                        {
                            c'8.
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'4.
                        }
                    } % measure
                    { % measure
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4
                        }
                    } % measure
                }

            Divisions less than twice the duration of a quarter note are filled
            with a single attack.

        ..  container:: example

            Fills divisions with half notes:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[2],
            ...     )

            >>> divisions = [(3, 16), (3, 8), (3, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 3/16
                        {
                            c'8.
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'4.
                        }
                    } % measure
                    { % measure
                        \time 3/4
                        {
                            c'2.
                        }
                    } % measure
                }

            Fills divisions less than twice the duration of a half note with a
            single attack.

        Returns tuple of nonnegative integer powers of two.
        '''
        if self._denominators:
            return list(self._denominators)

    @property
    def division_masks(self):
        r'''Gets division masks.

        ..  container:: example

            No division masks:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker()

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            Silences every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     division_masks=[
            ...         abjad.silence([0], 2),
            ...         ],
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            Sustains every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     division_masks=[
            ...         abjad.sustain([0], 2),
            ...         ],
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            Silences every output division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     division_masks=abjad.silence([0], 1),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        r4.
                    } % measure
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        r4.
                    } % measure
                }

        Set to division masks or none.
        '''
        superclass = super(EvenDivisionRhythmMaker, self)
        return superclass.division_masks

    @property
    def extra_counts_per_division(self):
        r'''Gets extra counts per division.

        Treats overly large and overly small values of
        `extra_counts_per_division` modularly. Denote by
        `unprolated_note_count` the number of unprolated notes included in any
        division (as though `extra_counts_per_division` were set to zero). Then
        the actual number of extra counts included per division is given by two
        formulas:

        * The actual number of extra counts included per division is given by
          ``extra_counts_per_division % unprolated_note_count`` when
          `extra_counts_per_division` is positive.

        * The actual number of extra counts included per division is given by
          the formula
          ``extra_counts_per_division % ceiling(unprolated_note_count / 2)``
          when `extra_counts_per_division` is negative.

        These formulas ensure that:

        * even very large and very small values of
          `extra_counts_per_division` produce valid output, and that

        * the values given as the rhythm-maker's `denominators` are always
          respected. A very large value of `extra_counts_per_division`, for
          example, never causes a `16`-denominated division to result 32nd or
          64th note rhythms; `16`-denominated divisions always produce 16th
          note rhythms.

        ..  container:: example

            Four missing counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[-4],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Three missing counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[-3],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Two missing counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[-2],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/3 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            One missing count per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[-1],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Neither missing nor extra counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=None,
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            One extra count per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[1],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        \times 2/3 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        \times 4/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Two extra counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[2],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        \times 4/6 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/7 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Three extra counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[3],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        \times 2/3 {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        {
                            c'16 [
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        \times 4/7 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }


        ..  container:: example

            Four extra counts per division:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     )

            >>> divisions = [(1, 16), (2, 16), (3, 16), (4, 16), (5, 16)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 1/16
                        {
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 2/16
                        {
                            c'16 [
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 5/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        Returns (possibly empty) tuple of integers or none.
        '''
        if self._extra_counts_per_division:
            return list(self._extra_counts_per_division)

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        ..  container:: example

            No logical tie masks:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker()

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            Silences every third logical tie:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     logical_tie_masks=[
            ...         abjad.silence([0], 3),
            ...         ],
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            r8
                            c'8 [
                            c'8 ]
                            r8
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8 ]
                            r8
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8 ]
                            r8
                            c'8
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8
                            r8
                            c'8
                        }
                    } % measure
                }

        ..  container:: example

            Silences every logical tie except the first two and last two:

            >>> pattern_1 = abjad.index_all()
            >>> pattern_2 = abjad.index_first(2)
            >>> pattern_3 = abjad.index_last(2)
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = abjad.SilenceMask(pattern)
            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     logical_tie_masks=mask,
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8 ]
                            r8
                            r8
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            r8
                            r8
                            r8
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            r8
                            r8
                            r8
                            r8
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            r8
                            c'8 [
                            c'8 ]
                        }
                    } % measure
                }

        ..  container:: example

            With ties across divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ~ ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ~ ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ~ ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

            Silences every fourth logical tie:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     logical_tie_masks=abjad.silence([3], 4),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                            r8
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            r8
                            c'8 [
                            c'8 ~ ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        {
                            c'8 [
                            c'8 ]
                            r8
                            c'8 ~
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    } % measure
                }

            Silencing the fourth logical tie produces two rests. Silencing the
            eighth logical tie produces only one rest.

        Returns patterns or none.
        '''
        superclass = super(EvenDivisionRhythmMaker, self)
        return superclass.logical_tie_masks

    @property
    def preferred_denominator(self):
        r'''Gets preferred denominator.

        ..  container:: example

            No preferred denominator:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     preferred_denominator=None,
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        \times 2/3 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        \times 2/3 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

            Expresses tuplet ratios in the usual way with numerator and
            denominator relatively prime.

        ..  container:: example

            Preferred denominator equal to 4:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     preferred_denominator=4,
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        \times 4/6 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        \times 4/6 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

            Preferred denominator equal to 8:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     preferred_denominator=8,
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        \times 8/12 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        \times 8/12 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

            Preferred denominator equal to 16:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     preferred_denominator=16,
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        \times 16/24 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        \times 16/24 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        ..  container:: example

            Preferred denominator taken from count of elements in tuplet:

            >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
            ...     denominators=[16],
            ...     extra_counts_per_division=[4],
            ...     preferred_denominator='from_counts',
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    { % measure
                        \time 4/8
                        \times 8/12 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 4/8
                        \times 8/12 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                    { % measure
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    } % measure
                }

        Defaults to none.

        Set to none or positive integer.

        Returns none or positive integer.
        '''
        return self._preferred_denominator

    @property
    def tuplet_specifier(self):
        r'''Gets tuplet spelling specifier.

        ..  note:: not yet implemented.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(EvenDivisionRhythmMaker, self)
        return superclass.tuplet_specifier
