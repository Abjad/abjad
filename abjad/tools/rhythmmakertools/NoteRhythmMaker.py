# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class NoteRhythmMaker(RhythmMaker):
    r'''Note rhythm-maker.

    ..  container:: example

        Makes notes equal to the duration of input divisions. Adds ties where
        necessary:

        ::

            >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = rhythm_maker._get_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/8
                    c'2 ~
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_burnish_specifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        burnish_specifier=None,
        division_masks=None,
        duration_spelling_specifier=None,
        logical_tie_masks=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        if burnish_specifier is not None:
            prototype = rhythmmakertools.BurnishSpecifier
            assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls note rhythm-maker on `divisions`.

        ..  container:: example

            **Example 1.** Calls rhythm-maker on divisions:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = [(5, 8), (3, 8)]
                >>> result = rhythm_maker(divisions)
                >>> for x in result:
                ...     x
                Selection([Note("c'2"), Note("c'8")])
                Selection([Note("c'4.")])

        Returns list of selections. Each selection holds one or more notes.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    def __format__(self, format_specification=''):
        r'''Formats note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()
                >>> print(format(rhythm_maker))
                rhythmmakertools.NoteRhythmMaker()

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            ::

                >>> rhythmmakertools.NoteRhythmMaker()
                NoteRhythmMaker()

        Returns string.
        '''
        return super(NoteRhythmMaker, self).__repr__()

    ### PRIVATE METHODS ###

    def _apply_burnish_specifier(self, selections):
        if self.burnish_specifier is None:
            return selections
        elif self.burnish_specifier.outer_divisions_only:
            selections = self._burnish_outer_divisions(selections)
        else:
            selections = self._burnish_each_division(selections)
        return selections

    def _burnish_each_division(self, selections):
        message = 'NoteRhythmMaker does not yet implement'
        message += ' burnishing each division.'
        raise NotImplementedError(message)

    def _burnish_outer_divisions(self, selections):
        left_classes = self.burnish_specifier.left_classes
        left_counts = self.burnish_specifier.left_counts
        right_classes = self.burnish_specifier.right_classes
        right_counts = self.burnish_specifier.right_counts
        if left_counts:
            assert len(left_counts) == 1, repr(left_counts)
            left_count = left_counts[0]
        else:
            left_count = 0
        if right_counts:
            assert len(right_counts) == 1, repr(right_counts)
            right_count = right_counts[0]
        else:
            right_count = 0
        if left_count + right_count <= len(selections):
            middle_count = len(selections) - (left_count + right_count)
        elif left_count <= len(selections):
            right_count = len(selections) - left_count
            middle_count = 0
        else:
            left_count = len(selections)
            right_count = 0
            middle_count = 0
        assert left_count + middle_count + right_count == len(selections)
        new_selections = []
        left_classes = datastructuretools.CyclicTuple(left_classes)
        for i, selection in enumerate(selections[:left_count]):
            target_class = left_classes[i]
            new_selection = self._cast_selection(selection, target_class)
            new_selections.append(new_selection)
        if right_count:
            for selection in selections[left_count:-right_count]:
                new_selections.append(selection)
            right_classes = datastructuretools.CyclicTuple(right_classes)
            for i, selection in enumerate(selections[-right_count:]):
                target_class = right_classes[i]
                new_selection = self._cast_selection(selection, target_class)
                new_selections.append(new_selection)
        else:
            for selection in selections[left_count:]:
                new_selections.append(selection)
        return new_selections

    def _cast_selection(self, selection, target_class):
        new_selection = []
        for leaf in selection:
            new_leaf = target_class(leaf)
            new_selection.append(new_leaf)
        new_selection = selectiontools.Selection(new_selection)
        return new_selection

    def _make_music(self, divisions, rotation):
        from abjad.tools import rhythmmakertools
        selections = []
        duration_specifier = self._get_duration_spelling_specifier()
        tie_specifier = self._get_tie_specifier()
        tuplet_specifier = self._get_tuplet_spelling_specifier()
        for division in divisions:
            if (duration_specifier.spell_metrically == True or
                (duration_specifier.spell_metrically == 'unassignable' and
                not mathtools.is_assignable_integer(division.numerator))):
                meter = metertools.Meter(division)
                rhythm_tree_container = meter.root_node
                durations = [_.duration for _ in rhythm_tree_container]
            elif isinstance(duration_specifier.spell_metrically,
                rhythmmakertools.PartitionTable):
                partition_table = duration_specifier.spell_metrically
                durations = partition_table.respell_division(division)
            else:
                durations = [division]
            selection = scoretools.make_leaves(
                pitches=0,
                durations=durations,
                decrease_durations_monotonically=\
                    duration_specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    duration_specifier.forbidden_written_duration,
                is_diminution=tuplet_specifier.is_diminution,
                use_messiaen_style_ties=tie_specifier.use_messiaen_style_ties,
                )
            if (
                1 < len(selection) and
                not selection[0]._has_spanner(spannertools.Tie)
                ):
                tie = spannertools.Tie(
                    use_messiaen_style_ties=tie_specifier.use_messiaen_style_ties,
                    )
                attach(tie, selection[:])
            selections.append(selection)
        selections = self._apply_burnish_specifier(selections)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        selections = self._apply_division_masks(selections, rotation)
        if duration_specifier.rewrite_meter:
            selections = duration_specifier._rewrite_meter_(
                selections,
                divisions,
                use_messiaen_style_ties=tie_specifier.use_messiaen_style_ties,
                )
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier.

        ..  container:: example

            **Example 1.** Beams each division:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 32), (5, 32)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/32
                        c'8 ~ [
                        c'32 ]
                    }
                    {
                        c'8 ~ [
                        c'32 ]
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Beams divisions together:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 32), (5, 32)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/32
                        \set stemLeftBeamCount = #0
                        \set stemRightBeamCount = #1
                        c'8 [ ~
                        \set stemLeftBeamCount = #3
                        \set stemRightBeamCount = #1
                        c'32
                    }
                    {
                        \set stemLeftBeamCount = #1
                        \set stemRightBeamCount = #1
                        c'8 ~
                        \set stemLeftBeamCount = #3
                        \set stemRightBeamCount = #0
                        c'32 ]
                    }
                }

        ..  container:: example

            **Example 3.** Makes no beams:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=False,
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 32), (5, 32)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/32
                        c'8 ~
                        c'32
                    }
                    {
                        c'8 ~
                        c'32
                    }
                }

        Returns beam specifier.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier.

        ..  container:: example

            **Example 1.** Burnishes nothing:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                    {
                        \time 2/8
                        c'4
                    }
                    {
                        c'4
                    }
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                }

        ..  container:: example

            **Example 2.** Forces leaves of first division to be rests:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[1],
                ...         outer_divisions_only=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        r2
                        r8
                    }
                    {
                        \time 2/8
                        c'4
                    }
                    {
                        c'4
                    }
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                }

        ..  container:: example

            **Example 3.** Forces leaves of first two divisions to be rests:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[2],
                ...         outer_divisions_only=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        r2
                        r8
                    }
                    {
                        \time 2/8
                        r4
                    }
                    {
                        c'4
                    }
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                }

        ..  container:: example

            **Example 4.** Forces leaves of first and last divisions to rests:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[1],
                ...         right_classes=[Rest],
                ...         right_counts=[1],
                ...         outer_divisions_only=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        r2
                        r8
                    }
                    {
                        \time 2/8
                        c'4
                    }
                    {
                        c'4
                    }
                    {
                        \time 5/8
                        r2
                        r8
                    }
                }

        ..  note:: Currently only works when `outer_divisions_only` is true.

        Returns burnish specifier or none.
        '''
        return self._burnish_specifier

    @property
    def division_masks(self):
        r'''Gets division masks.

        ..  container:: example

            **Example 1.** No division masks:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 2.** Silences every other division:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         rhythmmakertools.SilenceMask(
                ...             pattern=patterntools.select_every([0], period=2),
                ...             ),
                ...         ],
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** Silences every output division:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[rhythmmakertools.silence_all()],
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            **Example 4.** Silences every output division and uses
            multimeasure rests:

            ::

                >>> mask = rhythmmakertools.SilenceMask(
                ...     pattern=patterntools.select_all(),
                ...     use_multimeasure_rests=True,
                ...     )
                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        R1 * 1/2
                    }
                    {
                        \time 3/8
                        R1 * 3/8
                    }
                    {
                        \time 4/8
                        R1 * 1/2
                    }
                    {
                        \time 3/8
                        R1 * 3/8
                    }
                }

        ..  container:: example

            **Example 5.** Silences every other output division except for the
            first and last:

            ::

                >>> pattern_1 = patterntools.select_every([0], period=2)
                >>> pattern_2 = patterntools.select([0, -1])
                >>> pattern = pattern_1 & ~pattern_2
                >>> mask = rhythmmakertools.SilenceMask(
                ...     pattern=pattern,
                ...     )
                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8), (2, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 2/8
                        c'4
                    }
                }

        Set to masks or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.division_masks

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier.

        ..  container:: example

            **Example 1.** Spells durations with the fewest number of glyphs:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 2.** Forbids notes with written duration greater than or
            equal to ``1/2``:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         forbidden_written_duration=Duration(1, 2),
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4 ~
                        c'4 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** Spells all divisions metrically when
            `spell_metrically` is true:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4 ~
                        c'4 ~
                        c'4
                    }
                    {
                        \time 6/16
                        c'8. ~ [
                        c'8. ]
                    }
                    {
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    }
                }

        ..  container:: example

            **Example 4.** Spells only unassignable durations metrically when
            `spell_metrically` is ``'unassignable'``:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'2.
                    }
                    {
                        \time 6/16
                        c'4.
                    }
                    {
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    }
                }

            ``9/16`` is spelled metrically because it is unassignable.
            The other durations are spelled with the fewest number of symbols
            possible.

        ..  container:: example

            **Example 5.** Spells durations with custom partition table:

            ::

                >>> partition_table = rhythmmakertools.PartitionTable([
                ...     (5, [3, 2]),
                ...     (9, [3, 3, 3]),
                ...     ])
                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=partition_table,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 16), (9, 16), (10, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/16
                        c'8. ~ [
                        c'8 ]
                    }
                    {
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    }
                    {
                        \time 10/16
                        c'4. ~
                        c'4
                    }
                }

        ..  container:: example

            **Example 4.** Rewrites meter:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         rewrite_meter=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'2.
                    }
                    {
                        \time 6/16
                        c'4.
                    }
                    {
                        \time 9/16
                        c'4. ~
                        c'8.
                    }
                }

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        ..  container:: example

            **Example 1.** No logical tie masks:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 2.** Silences every other logical tie:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     logical_tie_masks=rhythmmakertools.silence_every([0], period=2)
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** Silences all logical ties:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     logical_tie_masks=rhythmmakertools.silence_all(),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        Set to masks or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.logical_tie_masks
    
    @property
    def tie_specifier(self):
        r'''Gets tie specifier.

        ..  container:: example

            **Example 1.** Does not tie across divisions:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Ties across divisions:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2 ~
                    }
                    {
                        \time 3/8
                        c'4. ~
                    }
                    {
                        \time 4/8
                        c'2 ~
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** Patterns ties across divisions:

            ::

                >>> pattern = patterntools.Pattern(
                ...     indices=[0],
                ...     period=2,
                ...     )
                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2 ~
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 4/8
                        c'2 ~
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 4.** Uses Messiaen-style ties:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         use_messiaen_style_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 8), (9, 16), (5, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        \time 3/8
                        c'4. \repeatTie
                    }
                    {
                        \time 9/16
                        c'2 \repeatTie
                        c'16 \repeatTie
                    }
                    {
                        \time 5/16
                        c'4 \repeatTie
                        c'16 \repeatTie
                    }
                }

        ..  container:: example

            **Example 5.** Strips all ties:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         strip_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(7, 16), (1, 4), (5, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 1/4
                        c'4
                    }
                    {
                        \time 5/16
                        c'4
                        c'16
                    }
                }

        ..  container:: example

            **Example 6.** Spells durations metrically and then strips all
            ties:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         strip_ties=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(7, 16), (1, 4), (5, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'8. [
                        c'8
                        c'8 ]
                    }
                    {
                        \time 1/4
                        c'4
                    }
                    {
                        \time 5/16
                        c'8. [
                        c'8 ]
                    }
                }

        Returns tie specifier.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier.

        ..  container:: example

            **Example 1.** Spells tuplets as diminutions:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/14
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2 ~
                            c'8
                        }
                    }
                    {
                        \time 3/7
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2.
                        }
                    }
                }

            This is the default behavior.

        ..  container:: example

            **Example 2.** Spells tuplets as augmentations:

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         is_diminution=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = rhythm_maker._get_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/14
                        \tweak text #tuplet-number::calc-fraction-text
                        \tweak edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4 ~
                            c'16
                        }
                    }
                    {
                        \time 3/7
                        \tweak text #tuplet-number::calc-fraction-text
                        \tweak edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4.
                        }
                    }
                }

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.tuplet_spelling_specifier
