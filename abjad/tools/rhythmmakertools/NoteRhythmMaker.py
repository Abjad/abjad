from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class NoteRhythmMaker(RhythmMaker):
    r'''Note rhythm-maker.

    ..  container:: example

        Makes notes equal to the duration of input divisions. Adds ties where
        necessary:

        >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

        >>> divisions = [(5, 8), (3, 8)]
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
                    \time 5/8
                    c'2 ~
                    c'8
                } % measure
                { % measure
                    \time 3/8
                    c'4.
                } % measure
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
        duration_specifier=None,
        logical_tie_masks=None,
        tie_specifier=None,
        tuplet_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        if burnish_specifier is not None:
            prototype = rhythmmakertools.BurnishSpecifier
            assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls note rhythm-maker on `divisions`.

        ..  container:: example

            Calls rhythm-maker on divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
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

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> abjad.f(rhythm_maker)
            abjad.rhythmmakertools.NoteRhythmMaker()

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            >>> abjad.rhythmmakertools.NoteRhythmMaker()
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
        import abjad
        new_selection = []
        for leaf in selection:
            new_leaf = target_class(leaf)
            new_selection.append(new_leaf)
        new_selection = abjad.select(new_selection)
        return new_selection

    def _make_music(self, divisions, rotation):
        import abjad
        from abjad.tools import rhythmmakertools
        selections = []
        duration_specifier = self._get_duration_specifier()
        tie_specifier = self._get_tie_specifier()
        tuplet_specifier = self._get_tuplet_specifier()
        leaf_maker = abjad.LeafMaker(
            decrease_monotonic=duration_specifier.decrease_monotonic,
            forbidden_duration=duration_specifier.forbidden_duration,
            is_diminution=tuplet_specifier.is_diminution,
            repeat_ties=tie_specifier.repeat_ties,
            )
        for division in divisions:
            if (duration_specifier.spell_metrically is True or
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
            selection = leaf_maker(pitches=0, durations=durations)
            if (1 < len(selection) and
                not selection[0]._has_spanner(spannertools.Tie)):
                tie = spannertools.Tie(
                    repeat_ties=tie_specifier.repeat_ties,
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
                repeat_ties=tie_specifier.repeat_ties,
                )
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier.

        ..  container:: example

            Beams each division:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_each_division=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 32), (5, 32)]
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
                        \time 5/32
                        c'8 ~ [
                        c'32 ]
                    } % measure
                    { % measure
                        c'8 ~ [
                        c'32 ]
                    } % measure
                }

        ..  container:: example

            Beams divisions together:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 32), (5, 32)]
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
                        \time 5/32
                        \set stemLeftBeamCount = #0
                        \set stemRightBeamCount = #1
                        c'8 ~ [
                        \set stemLeftBeamCount = #3
                        \set stemRightBeamCount = #1
                        c'32
                    } % measure
                    { % measure
                        \set stemLeftBeamCount = #1
                        \set stemRightBeamCount = #1
                        c'8 ~
                        \set stemLeftBeamCount = #3
                        \set stemRightBeamCount = #0
                        c'32 ]
                    } % measure
                }

        ..  container:: example

            Makes no beams:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...         beam_divisions_together=False,
            ...         beam_each_division=False,
            ...         ),
            ...     )

            >>> divisions = [(5, 32), (5, 32)]
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
                        \time 5/32
                        c'8 ~
                        c'32
                    } % measure
                    { % measure
                        c'8 ~
                        c'32
                    } % measure
                }

        Returns beam specifier.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier.

        ..  container:: example

            Burnishes nothing:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

            >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
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
                        \time 5/8
                        c'2 ~
                        c'8
                    } % measure
                    { % measure
                        \time 2/8
                        c'4
                    } % measure
                    { % measure
                        c'4
                    } % measure
                    { % measure
                        \time 5/8
                        c'2 ~
                        c'8
                    } % measure
                }

        ..  container:: example

            Forces leaves of first division to be rests:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         outer_divisions_only=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
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
                        \time 5/8
                        r2
                        r8
                    } % measure
                    { % measure
                        \time 2/8
                        c'4
                    } % measure
                    { % measure
                        c'4
                    } % measure
                    { % measure
                        \time 5/8
                        c'2 ~
                        c'8
                    } % measure
                }

        ..  container:: example

            Forces leaves of first two divisions to be rests:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[2],
            ...         outer_divisions_only=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
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
                        \time 5/8
                        r2
                        r8
                    } % measure
                    { % measure
                        \time 2/8
                        r4
                    } % measure
                    { % measure
                        c'4
                    } % measure
                    { % measure
                        \time 5/8
                        c'2 ~
                        c'8
                    } % measure
                }

        ..  container:: example

            Forces leaves of first and last divisions to rests:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     burnish_specifier=abjad.rhythmmakertools.BurnishSpecifier(
            ...         left_classes=[abjad.Rest],
            ...         left_counts=[1],
            ...         right_classes=[abjad.Rest],
            ...         right_counts=[1],
            ...         outer_divisions_only=True,
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (2, 8), (2, 8), (5, 8)]
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
                        \time 5/8
                        r2
                        r8
                    } % measure
                    { % measure
                        \time 2/8
                        c'4
                    } % measure
                    { % measure
                        c'4
                    } % measure
                    { % measure
                        \time 5/8
                        r2
                        r8
                    } % measure
                }

        ..  note:: Currently only works when `outer_divisions_only` is true.

        Returns burnish specifier or none.
        '''
        return self._burnish_specifier

    @property
    def division_masks(self):
        r'''Gets division masks.

        ..  container:: example

            No division masks:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

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
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Silences every other division:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         abjad.rhythmmakertools.SilenceMask(
            ...             pattern=abjad.index([0], 2),
            ...             ),
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
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Silences every output division:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[abjad.silence([0], 1)],
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

        ..  container:: example

            Silences every output division and uses multimeasure rests:

            >>> mask = abjad.rhythmmakertools.SilenceMask(
            ...     pattern=abjad.index_all(),
            ...     use_multimeasure_rests=True,
            ...     )
            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
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
                        R1 * 1/2
                    } % measure
                    { % measure
                        \time 3/8
                        R1 * 3/8
                    } % measure
                    { % measure
                        \time 4/8
                        R1 * 1/2
                    } % measure
                    { % measure
                        \time 3/8
                        R1 * 3/8
                    } % measure
                }

        ..  container:: example

            Silences every other output division except for the first and last:

            >>> pattern_1 = abjad.index([0], 2)
            >>> pattern_2 = abjad.index([0, -1])
            >>> pattern = pattern_1 & ~pattern_2
            >>> mask = abjad.rhythmmakertools.SilenceMask(
            ...     pattern=pattern,
            ...     )
            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )

            >>> divisions = [(4, 8), (3, 8), (4, 8), (3, 8), (2, 8)]
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
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                    { % measure
                        \time 2/8
                        c'4
                    } % measure
                }

        Set to masks or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.division_masks

    @property
    def duration_specifier(self):
        r'''Gets duration spelling specifier.

        ..  container:: example

            Spells durations with the fewest number of glyphs:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

            >>> divisions = [(5, 8), (3, 8)]
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
                        \time 5/8
                        c'2 ~
                        c'8
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Forbids notes with written duration greater than or equal to
            ``1/2``:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         forbidden_duration=(1, 2),
            ...         ),
            ...     )

            >>> divisions = [(5, 8), (3, 8)]
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
                        \time 5/8
                        c'4 ~
                        c'4 ~
                        c'8
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Spells all divisions metrically when `spell_metrically` is true:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         spell_metrically=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 4), (6, 16), (9, 16)]
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
                        \time 3/4
                        c'4 ~
                        c'4 ~
                        c'4
                    } % measure
                    { % measure
                        \time 6/16
                        c'8. ~ [
                        c'8. ]
                    } % measure
                    { % measure
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    } % measure
                }

        ..  container:: example

            Spells only unassignable durations metrically when
            `spell_metrically` is ``'unassignable'``:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         spell_metrically='unassignable',
            ...         ),
            ...     )

            >>> divisions = [(3, 4), (6, 16), (9, 16)]
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
                        \time 3/4
                        c'2.
                    } % measure
                    { % measure
                        \time 6/16
                        c'4.
                    } % measure
                    { % measure
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    } % measure
                }

            ``9/16`` is spelled metrically because it is unassignable.
            The other durations are spelled with the fewest number of symbols
            possible.

        ..  container:: example

            Spells durations with custom partition table:

            >>> partition_table = abjad.rhythmmakertools.PartitionTable([
            ...     (5, [3, 2]),
            ...     (9, [3, 3, 3]),
            ...     ])
            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         spell_metrically=partition_table,
            ...         ),
            ...     )

            >>> divisions = [(5, 16), (9, 16), (10, 16)]
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
                        \time 5/16
                        c'8. ~ [
                        c'8 ]
                    } % measure
                    { % measure
                        \time 9/16
                        c'8. ~ [
                        c'8. ~
                        c'8. ]
                    } % measure
                    { % measure
                        \time 10/16
                        c'4. ~
                        c'4
                    } % measure
                }

        ..  container:: example

            Rewrites meter:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         rewrite_meter=True,
            ...         ),
            ...     )

            >>> divisions = [(3, 4), (6, 16), (9, 16)]
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
                        \time 3/4
                        c'2.
                    } % measure
                    { % measure
                        \time 6/16
                        c'4.
                    } % measure
                    { % measure
                        \time 9/16
                        c'4. ~
                        c'8.
                    } % measure
                }

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_specifier.fget(self)

    @property
    def logical_tie_masks(self):
        r'''Gets logical tie masks.

        ..  container:: example

            No logical tie masks:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

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
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Silences every other logical tie:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     logical_tie_masks=abjad.silence([0], 2),
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
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        r2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Silences all logical ties:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     logical_tie_masks=abjad.silence([0], 1),
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

        Set to masks or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.logical_tie_masks

    @property
    def tie_specifier(self):
        r'''Gets tie specifier.

        ..  container:: example

            Does not tie across divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=False,
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
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        c'2
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Ties across divisions:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
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
                        c'2 ~
                    } % measure
                    { % measure
                        \time 3/8
                        c'4. ~
                    } % measure
                    { % measure
                        \time 4/8
                        c'2 ~
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Patterns ties across divisions:

            >>> pattern = abjad.Pattern(
            ...     indices=[0],
            ...     period=2,
            ...     )
            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
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
                        c'2 ~
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                    { % measure
                        \time 4/8
                        c'2 ~
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }

        ..  container:: example

            Uses Messiaen-style ties:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         repeat_ties=True,
            ...         ),
            ...     )

            >>> divisions = [(4, 8), (3, 8), (9, 16), (5, 16)]
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
                        c'4. \repeatTie
                    } % measure
                    { % measure
                        \time 9/16
                        c'2 \repeatTie
                        c'16 \repeatTie
                    } % measure
                    { % measure
                        \time 5/16
                        c'4 \repeatTie
                        c'16 \repeatTie
                    } % measure
                }

        ..  container:: example

            Strips all ties:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         strip_ties=True,
            ...         ),
            ...     )

            >>> divisions = [(7, 16), (1, 4), (5, 16)]
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
                        \time 7/16
                        c'4..
                    } % measure
                    { % measure
                        \time 1/4
                        c'4
                    } % measure
                    { % measure
                        \time 5/16
                        c'4
                        c'16
                    } % measure
                }

        ..  container:: example

            Spells durations metrically and then strips all ties:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     duration_specifier=abjad.rhythmmakertools.DurationSpecifier(
            ...         spell_metrically=True,
            ...         ),
            ...     tie_specifier=abjad.rhythmmakertools.TieSpecifier(
            ...         strip_ties=True,
            ...         ),
            ...     )

            >>> divisions = [(7, 16), (1, 4), (5, 16)]
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
                        \time 7/16
                        c'8. [
                        c'8
                        c'8 ]
                    } % measure
                    { % measure
                        \time 1/4
                        c'4
                    } % measure
                    { % measure
                        \time 5/16
                        c'8. [
                        c'8 ]
                    } % measure
                }

        Returns tie specifier.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tuplet_specifier(self):
        r'''Gets tuplet spelling specifier.

        ..  container:: example

            Spells tuplets as diminutions:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()

            >>> divisions = [(5, 14), (3, 7)]
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
                        \time 5/14
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2 ~
                            c'8
                        }
                    } % measure
                    { % measure
                        \time 3/7
                        \tweak edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2.
                        }
                    } % measure
                }

        ..  container:: example

            Spells tuplets as augmentations:

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     tuplet_specifier=abjad.rhythmmakertools.TupletSpecifier(
            ...         is_diminution=False,
            ...         ),
            ...     )

            >>> divisions = [(5, 14), (3, 7)]
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
                        \time 5/14
                        \tweak text #tuplet-number::calc-fraction-text
                        \tweak edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4 ~
                            c'16
                        }
                    } % measure
                    { % measure
                        \time 3/7
                        \tweak text #tuplet-number::calc-fraction-text
                        \tweak edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4.
                        }
                    } % measure
                }

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.tuplet_specifier
