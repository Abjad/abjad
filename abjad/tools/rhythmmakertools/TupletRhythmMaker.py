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


class TupletRhythmMaker(RhythmMaker):
    r'''Tuplet rhythm-maker.

    ..  container:: example

        Makes tuplets with ``3:2`` ratios:

        ::

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(3, 2)],
            ...     )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16)]
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
                    \time 1/2
                    \times 4/5 {
                        c'4.
                        c'4
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'4.
                        c'4
                    }
                }
                {
                    \time 5/16
                    {
                        c'8. [
                        c'8 ]
                    }
                }
            }

    ..  container:: example

        Makes tuplets with alternating ``1:-1`` and ``3:1`` ratios:

        ::

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, -1), (3, 1)],
            ...     )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16)]
            >>> selections = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 1/2
                    {
                        c'4
                        r4
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4.
                        c'8
                    }
                }
                {
                    \time 5/16
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 5/6 {
                        c'8.
                        r8.
                    }
                }
            }

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a list of selections as
    output (structured one selection per division). Each selection wraps a
    single fixed-duration tuplet.

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tuplet_ratios',
        '_tuplet_spelling_specifier',
        )

    _class_name_abbreviation = 'T'

    _human_readable_class_name = 'tuplet rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        tuplet_ratios=((1, 1), (1, 2), (1, 3)),
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        if tuplet_ratios is not None:
            tuplet_ratios = tuple(mathtools.Ratio(x) for x in tuplet_ratios)
        self._tuplet_ratios = tuplet_ratios

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls tuplet rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = maker(divisions)
                >>> for division in music:
                ...     division
                Selection(FixedDurationTuplet(Duration(1, 2), "c'4 r4"),)
                Selection(FixedDurationTuplet(Duration(3, 8), "c'4. c'8"),)
                Selection(FixedDurationTuplet(Duration(5, 16), "c'8. r8."),)

        Returns list of selections structured one selection per division.
        Each selection wraps a single fixed-duration tuplet.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats tuplet rhythm-maker.

        ..  container:: example

            ::

                rhythmmakertools.TupletRhythmMaker(
                    tuplet_ratios=(
                        mathtools.Ratio(1, -1),
                        mathtools.Ratio(3, 1),
                        ),
                    )

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        tuplets = []
        if not isinstance(seeds, int):
            seeds = 0
        tuplet_ratios = datastructuretools.CyclicTuple(
            sequencetools.rotate_sequence(self.tuplet_ratios, seeds)
            )

#        beam_specifier = self.beam_specifier
#        if beam_specifier is None:
#            beam_specifier = rhythmmakertools.BeamSpecifier()

        tuplet_spelling_specifier = self.tuplet_spelling_specifier
        if tuplet_spelling_specifier is None:
            tuplet_spelling_specifier = \
                rhythmmakertools.TupletSpellingSpecifier()
        for duration_index, duration_pair in enumerate(duration_pairs):
            ratio = tuplet_ratios[duration_index]
            duration = durationtools.Duration(duration_pair)
            tuplet = self._make_tuplet(
                duration,
                ratio,
                avoid_dots=tuplet_spelling_specifier.avoid_dots,
                is_diminution=tuplet_spelling_specifier.is_diminution,
                )

#            if beam_specifier.beam_each_division:
#                beam = spannertools.MultipartBeam()
#                attach(beam, tuplet)

            tuplets.append(tuplet)

#        if beam_specifier.beam_divisions_together:
#            beam = spannertools.MultipartBeam()
#            attach(beam, tuplets)

        selections = [selectiontools.Selection(x) for x in tuplets]
        self._apply_beam_specifier(selections)
        return selections

    def _make_tuplet(
        self,
        duration,
        ratio,
        avoid_dots=False,
        is_diminution=True,
        ):
        tuplet = scoretools.Tuplet.from_duration_and_ratio(
            duration,
            ratio,
            avoid_dots=avoid_dots,
            is_diminution=is_diminution,
            )
        return tuplet

    ### PUBLIC PROPERTIES ###

    @property
    def beam_specifier(self):
        r'''Gets beam specifier of tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** Beams each division:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1, 2, 1, 1), (3, 1, 1)],
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_each_division=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 16), (3, 16), (6, 16), (4, 16)]
                >>> selections = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file)  # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            c'16. [
                            c'16.
                            c'8.
                            c'16.
                            c'16. ]
                        }
                    }
                    {
                        \time 3/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8. [
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 6/16
                        {
                            c'16 [
                            c'16
                            c'8
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'8. [
                            c'16
                            c'16 ]
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Beams divisions together:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1, 2, 1, 1), (3, 1, 1)],
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 16), (3, 16), (6, 16), (4, 16)]
                >>> selections = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file)  # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #2
                            c'16. [
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16.
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8.
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16.
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16.
                        }
                    }
                    {
                        \time 3/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8.
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16
                        }
                    }
                    {
                        \time 6/16
                        {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #1
                            c'16
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8.
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #2
                            c'16
                            \set stemLeftBeamCount = #2
                            \set stemRightBeamCount = #0
                            c'16 ]
                        }
                    }
                }

        ..  container:: example

            **Example 3.** Beams nothing:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1, 2, 1, 1), (3, 1, 1)],
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=False,
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 16), (3, 16), (6, 16), (4, 16)]
                >>> selections = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file)  # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            c'16.
                            c'16.
                            c'8.
                            c'16.
                            c'16.
                        }
                    }
                    {
                        \time 3/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8.
                            c'16
                            c'16
                        }
                    }
                    {
                        \time 6/16
                        {
                            c'16
                            c'16
                            c'8
                            c'16
                            c'16
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'8.
                            c'16
                            c'16
                        }
                    }
                }

        Ignores `beam_each_division` when `beam_division_together` is true.

        Returns beam specifier or none.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** Ties nothing:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1)],
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
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
                        \time 1/2
                        \times 4/5 {
                            c'4
                            c'4.
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16.
                            r8.
                            c'16.
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'8 [
                            c'8. ]
                        }
                    }
                }

            This is the default behavior.

        ..  container:: example

            **Example 2.** Ties across all divisions:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1)],
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
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
                        \time 1/2
                        \times 4/5 {
                            c'4
                            c'4. ~
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16.
                            r8.
                            c'16. ~
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'8 [
                            c'8. ]
                        }
                    }
                }

        Returns tie specifier or none.
        '''
        return RhythmMaker.tie_specifier.fget(self)

    @property
    def tuplet_ratios(self):
        r'''Gets ratio talea of tuplet rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1)],
                ...     )
                >>> maker.tuplet_ratios
                (Ratio(2, 3), Ratio(1, -2, 1))

        Returns tuple of ratios.
        '''
        return self._tuplet_ratios

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of tuplet rhythm-maker.

        Returns tuplet spelling specifier.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.tuplet_spelling_specifier

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses tuplet rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1)],
                ...     )
                >>> reversed_maker = maker.reverse()

            ::

                >>> print(format(reversed_maker))
                rhythmmakertools.TupletRhythmMaker(
                    tuplet_ratios=(
                        mathtools.Ratio(1, -2, 1),
                        mathtools.Ratio(3, 2),
                        ),
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = reversed_maker(divisions)
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
                        \time 1/2
                        {
                            c'8
                            r4
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            c'4
                        }
                    }
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16.
                            r8.
                            c'16.
                        }
                    }
                }

        Defined equal to copy of maker with `tuplet_ratios` and
        `duration_spelling_specifier` reversed.

        Returns new tuplet rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        tuplet_ratios = []
        for ratio in reversed(self.tuplet_ratios):
            ratio = mathtools.Ratio([x for x in reversed(ratio)])
            tuplet_ratios.append(ratio)
        tuplet_ratios = tuple(tuplet_ratios)
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        specifier = specifier.reverse()
        maker = new(
            self,
            tuplet_ratios=tuplet_ratios,
            duration_spelling_specifier=specifier,
            )
        return maker

    def rotate(self, n=0):
        r'''Rotates tuplet rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1), (1, 2, 3)],
                ...     )
                >>> rotated_maker = maker.rotate(n=1)

            ::

                >>> print(format(rotated_maker))
                rhythmmakertools.TupletRhythmMaker(
                    tuplet_ratios=(
                        mathtools.Ratio(3, 1, 2),
                        mathtools.Ratio(3, 2),
                        mathtools.Ratio(1, 1, -2),
                        ),
                    )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = rotated_maker(divisions)
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
                        \time 1/2
                        \times 2/3 {
                            c'4.
                            c'8
                            c'4
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            c'4
                        }
                    }
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16. [
                            c'16. ]
                            r8.
                        }
                    }
                }

        Returns new tuplet rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        tuplet_ratios = []
        for ratio in sequencetools.rotate_sequence(self.tuplet_ratios, n):
            ratio = sequencetools.rotate_sequence(ratio, n)
            ratio = mathtools.Ratio(ratio)
            tuplet_ratios.append(ratio)
        tuplet_ratios = tuple(tuplet_ratios)
        maker = new(
            self,
            tuplet_ratios=tuplet_ratios,
            )
        return maker