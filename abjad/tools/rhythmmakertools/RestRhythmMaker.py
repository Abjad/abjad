# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import new


class RestRhythmMaker(RhythmMaker):
    r'''Rest rhythm-maker.

    ..  container:: example

        Makes rests equal to the duration of input divisions.

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker()

        ::

            >>> divisions = [(5, 16), (3, 8)]
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
                    r4
                    r16
                }
                {
                    \time 3/8
                    r4.
                }
            }

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'R'

    _human_readable_class_name = 'rest rhythm-maker'

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls rest rhythm-maker on `divisions`.

        ..  container:: example

            **Example 1.** With power-of-two durations:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()

            ::

                >>> divisions = [(5, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/16
                        r4
                        r16
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            **Example 2.** With non-power-of-two divisions:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> score_block = lilypond_file.items[-1]
                >>> score = score_block.items[0]
                >>> staff = score[-1]
                >>> override(staff).tuplet_bracket.staff_padding = 2.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff \with {
                    \override TupletBracket #'staff-padding = #2.5
                } {
                    {
                        \time 5/14
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            r2
                            r8
                        }
                    }
                    {
                        \time 3/7
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            r2.
                        }
                    }
                }

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print(format(maker))
                rhythmmakertools.RestRhythmMaker()

        Returns string.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import rhythmmakertools
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='duration_spelling_specifier',
                command='dss',
                editor=rhythmmakertools.DurationSpellingSpecifier,
                ),
            )

    ### PRIVATE METHODS ###

    def _make_music(self, divisions, seeds):
        from abjad.tools import rhythmmakertools
        selections = []
        duration_specifier = self.duration_spelling_specifier
        if duration_specifier is None:
            duration_specifier = rhythmmakertools.DurationSpellingSpecifier()
        tuplet_specifier = self.tuplet_spelling_specifier
        if tuplet_specifier is None:
            tuplet_specifier = rhythmmakertools.TupletSpellingSpecifier()
        for division in divisions:
            if (duration_specifier.spell_metrically == True or
                (duration_specifier.spell_metrically == 'unassignable' and
                not mathtools.is_assignable_integer(division.numerator))):
                meter = metertools.Meter(division)
                rhythm_tree_container = meter.root_node
                durations = [_.duration for _ in rhythm_tree_container]
            else:
                durations = [division]
            selection = scoretools.make_leaves(
                pitches=None,
                durations=durations,
                decrease_durations_monotonically=\
                    duration_specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    duration_specifier.forbidden_written_duration,
                is_diminution=tuplet_specifier.is_diminution,
                )
            selections.append(selection)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Rest rhythm-maker ignores beam specifier.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()
                >>> maker.beam_specifier is None
                True

        Returns none.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of rest rhythm-maker.

        ..  container:: example

            **Example 1.** Spells durations with the fewest number of glyphs:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()

            ::

                >>> divisions = [(5, 16), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            This is the default behavior.

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> print(format(staff))
                \new RhythmicStaff {
                    {
                        \time 5/16
                        r4
                        r16
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            **Example 2.** Forbids rests with written duration greater than or 
            equal to ``1/4``:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         forbidden_written_duration=Duration(1, 4),
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 16), (3, 8)]
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
                        r8
                        r8
                        r16
                    }
                    {
                        \time 3/8
                        r8
                        r8
                        r8
                    }
                }

        ..  container:: example

            **Example 3.** Spells all durations metrically when
            `spell_metrically` is true:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
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
                        \time 3/4
                        r4
                        r4
                        r4
                    }
                    {
                        \time 6/16
                        r8.
                        r8.
                    }
                    {
                        \time 9/16
                        r8.
                        r8.
                        r8.
                    }
                }

        ..  container:: example

            **Example 4.** Spells unassignable durations metrically when
            `spell_metrically` is ``'unassignable'``:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
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
                        \time 3/4
                        r2.
                    }
                    {
                        \time 6/16
                        r4.
                    }
                    {
                        \time 9/16
                        r8.
                        r8.
                        r8.
                    }
                }

            ``9/16`` is spelled metrically because it is unassignable.
            The other durations are spelled with the fewest number of symbols
            possible.

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    @property
    def tie_specifier(self):
        r'''Rest rhythm-maker ignores tie specifier.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()
                >>> maker.tie_specifier is None
                True

        Returns none.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.tie_specifier

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of rest rhythm-maker.

        ..  container:: example

            **Example 1.** Spells tuplets as diminutions:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> score_block = lilypond_file.items[-1]
                >>> score = score_block.items[0]
                >>> staff = score[-1]
                >>> override(staff).tuplet_bracket.staff_padding = 2.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff \with {
                    \override TupletBracket #'staff-padding = #2.5
                } {
                    {
                        \time 5/14
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            r2
                            r8
                        }
                    }
                    {
                        \time 3/7
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            r2.
                        }
                    }
                }

            This is the default behavior.

        ..  container:: example

            **Example 2.** Spells tuplets as augmentations:

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker(
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         is_diminution=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> score_block = lilypond_file.items[-1]
                >>> score = score_block.items[0]
                >>> staff = score[-1]
                >>> override(staff).tuplet_bracket.staff_padding = 2.5
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff \with {
                    \override TupletBracket #'staff-padding = #2.5
                } {
                    {
                        \time 5/14
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 8/7 {
                            r4
                            r16
                        }
                    }
                    {
                        \time 3/7
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 8/7 {
                            r4.
                        }
                    }
                }

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.tuplet_spelling_specifier

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rest rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()
                >>> reversed_maker = maker.reverse()

            ::

                >>> print(format(reversed_maker))
                rhythmmakertools.RestRhythmMaker(
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(5, 16), (3, 8)]
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
                        r4
                        r16
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        Returns new rest rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self.duration_spelling_specifier
        if duration_spelling_specifier is None:
            default = rhythmmakertools.DurationSpellingSpecifier()
            duration_spelling_specifier = default
        duration_spelling_specifier = duration_spelling_specifier.reverse()
        arguments = {
            'duration_spelling_specifier': duration_spelling_specifier,
            }
        result = new(self, **arguments)
        return result