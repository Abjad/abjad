# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import inspect_


class TupletRhythmMaker(RhythmMaker):
    r'''Tuplet rhythm-maker.

    ..  container:: example

        **Example 1.** Makes tuplets with ``3:2`` ratios:

        ::

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(3, 2)],
            ...     )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                {
                    {
                        c'8. [
                        c'8 ]
                    }
                }
            }

    ..  container:: example

        **Example 2.** Makes tuplets with alternating ``1:-1`` and ``3:1`` 
        ratios:

        ::

            >>> maker = rhythmmakertools.TupletRhythmMaker(
            ...     tuplet_ratios=[(1, -1), (3, 1)],
            ...     )

        ::

            >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                {
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 5/8 {
                        c'4.
                        c'8
                    }
                }
            }

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a list of selections as
    output. Output structured one selection per division with each selection
    wrapping a single fixed-duration tuplet.

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_preferred_denominator',
        '_tuplet_ratios',
        '_tuplet_spelling_specifier',
        )

    _class_name_abbreviation = 'T'

    _human_readable_class_name = 'tuplet rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        tuplet_ratios=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        output_masks=None,
        preferred_denominator=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            output_masks=output_masks,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        if tuplet_ratios is not None:
            tuplet_ratios = tuple(mathtools.Ratio(x) for x in tuplet_ratios)
        self._tuplet_ratios = tuplet_ratios
        if preferred_denominator is not None:
            prototype = (durationtools.Duration, int)
            assert (preferred_denominator == 'divisions' or
                isinstance(preferred_denominator, prototype))
        self._preferred_denominator = preferred_denominator

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls tuplet rhythm-maker on `divisions`.

        ..  container:: example

            **Example 1.** Calls tuplet rhythm-maker with one ratio:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, 2)],
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                    {
                        {
                            c'8. [
                            c'8 ]
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Calls tuplet rhythm-maker on two ratios:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, -1), (3, 1)],
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'4.
                            c'8
                        }
                    }
                }

        Returns list of selections structured one selection per division.
        Each selection wraps a single fixed-duration tuplet.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    def __format__(self, format_specification=''):
        r'''Formats tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** Formats tuplet rhythm-maker with one ratio:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, 2)],
                ...     )

            ::

                >>> print(format(maker))
                rhythmmakertools.TupletRhythmMaker(
                    tuplet_ratios=(
                        mathtools.Ratio((3, 2)),
                        ),
                    )

        ..  container:: example

            **Example 2.** Formats tuplet rhythm-maker with two ratios:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, -1), (3, 1)],
                ...     )

            ::

                >>> print(format(maker))
                rhythmmakertools.TupletRhythmMaker(
                    tuplet_ratios=(
                        mathtools.Ratio((1, -1)),
                        mathtools.Ratio((3, 1)),
                        ),
                    )

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, divisions, rotation):
        tuplets = []
        for division in divisions:
            assert isinstance(division, durationtools.Division), repr(division)
        if not isinstance(rotation, int):
            rotation = 0
        tuplet_ratios = datastructuretools.CyclicTuple(
            sequencetools.rotate_sequence(self.tuplet_ratios, rotation)
            )
        tuplet_spelling_specifier = self._get_tuplet_spelling_specifier()
        for duration_index, division in enumerate(divisions):
            ratio = tuplet_ratios[duration_index]
            duration = durationtools.Duration(division)
            tuplet = self._make_tuplet(
                duration,
                ratio,
                avoid_dots=tuplet_spelling_specifier.avoid_dots,
                is_diminution=tuplet_spelling_specifier.is_diminution,
                )
            if self.preferred_denominator is None:
                pass
            elif self.preferred_denominator == 'divisions':
                tuplet.preferred_denominator = division.numerator
            elif isinstance(
                self.preferred_denominator, durationtools.Duration):
                unit_duration = self.preferred_denominator
                assert unit_duration.numerator == 1
                duration = inspect_(tuplet).get_duration()
                denominator = unit_duration.denominator
                nonreduced_fraction = duration.with_denominator(denominator)
                tuplet.preferred_denominator = nonreduced_fraction.numerator
            elif mathtools.is_positive_integer(self.preferred_denominator):
                tuplet.preferred_denominator = self.preferred_denominator
            else:
                raise ValueError(self.preferred_denominator)
            tuplets.append(tuplet)
        selections = [selectiontools.Selection(x) for x in tuplets]
        self._apply_beam_specifier(selections)
        selections = self._apply_output_masks(selections, rotation)
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

                >>> divisions = [(5, 8), (3, 8), (6, 8), (4, 8)]
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
                        \time 5/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            c'8. [
                            c'8. ]
                            c'4.
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 6/8
                        {
                            c'8 [
                            c'8 ]
                            c'4
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'4.
                            c'8 [
                            c'8 ]
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

                >>> divisions = [(5, 8), (3, 8), (6, 8), (4, 8)]
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
                        \time 5/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #1
                            c'8. [
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8. ]
                            c'4.
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #1
                            c'8. [
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8. ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #1
                            c'8 [
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8
                        }
                    }
                    {
                        \time 6/8
                        {
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8 ]
                            c'4
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #1
                            c'8 [
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #1
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'4.
                            \set stemLeftBeamCount = #0
                            \set stemRightBeamCount = #1
                            c'8 [
                            \set stemLeftBeamCount = #1
                            \set stemRightBeamCount = #0
                            c'8 ]
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

                >>> divisions = [(5, 8), (3, 8), (6, 8), (4, 8)]
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
                        \time 5/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/9 {
                            c'8.
                            c'8.
                            c'4.
                            c'8.
                            c'8.
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            c'8
                            c'8
                        }
                    }
                    {
                        \time 6/8
                        {
                            c'8
                            c'8
                            c'4
                            c'8
                            c'8
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'4.
                            c'8
                            c'8
                        }
                    }
                }

        Ignores `beam_each_division` when `beam_division_together` is true.

        Set to beam specifier or none.

        Returns beam specifier or none.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.beam_specifier

    @property
    def output_masks(self):
        r'''Gets output masks of tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** No output masks:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(4, 1)],
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=False,
                ...         beam_each_division=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
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
                        \time 3/8
                        \times 4/5 {
                            c'4.
                            c'16.
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'2
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \times 4/5 {
                            c'4.
                            c'16.
                        }
                    }
                    {
                        \time 4/8
                        \times 4/5 {
                            c'2
                            c'8
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Masks every other output division:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(4, 1)],
                ...     beam_specifier=rhythmmakertools.BeamSpecifier(
                ...         beam_divisions_together=False,
                ...         beam_each_division=False,
                ...         ),
                ...     output_masks=[
                ...         rhythmmakertools.SilenceMask(
                ...             indices=[1],
                ...             period=2,
                ...             ),
                ...         ],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
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
                        \time 3/8
                        \times 4/5 {
                            c'4.
                            c'16.
                        }
                    }
                    {
                        \time 4/8
                        r2
                    }
                    {
                        \time 3/8
                        \times 4/5 {
                            c'4.
                            c'16.
                        }
                    }
                    {
                        \time 4/8
                        r2
                    }
                }

        Set to output masks or none.

        Returns output masks or none.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.output_masks

    @property
    def preferred_denominator(self):
        r'''Gets preferred denominator of tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** Tuplet numerators and denominators are reduced to
            numbers that are relatively prime when `preferred_denominator` is
            set to none. This means that ratios like ``6:4`` and ``10:8`` are
            not possible:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=None,
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** The preferred denominator of each tuplet is set to
            the numerator of the division that generates the tuplet when
            `preferred_denominator` is set to the string ``'divisions'``. This
            means that the tuplet numerator and denominator are not necessarily
            relatively prime. This also means that ratios like ``6:4`` and
            ``10:8`` are possible:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator='divisions',
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            **Example 3a.** The preferred denominator of each tuplet is set in
            terms of a unit duration when `preferred_denominator` is set to a
            duration. The setting does not affect the first tuplet:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=Duration(1, 16),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 6/10 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

            **Example 3b.** Sets the preferred denominator of each tuplet in 
            terms 32nd notes. The setting affects all tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=Duration(1, 32),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 16/20 {
                            c'8
                            c'2
                        }
                    }
                }

            **Example 3c.** Sets the preferred denominator each tuplet in terms
            64th notes. The setting affects all tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=Duration(1, 64),
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 8/10 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 16/20 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 24/40 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 32/40 {
                            c'8
                            c'2
                        }
                    }
                }

        ..  container:: example

            **Example 4a.** The preferred denominator of each tuplet is set
            directly when `preferred_denominator` is set to a positive integer.
            This example sets the preferred denominator of each tuplet to
            ``8``. Setting does not affect the third tuplet:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=8,
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 8/10 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 8/10 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 8/10 {
                            c'8
                            c'2
                        }
                    }
                }

            **Example 4b.** Sets the preferred denominator of each tuplet to
            ``12``. Setting affects all tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=12,
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 12/15 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 12/15 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 12/20 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 12/15 {
                            c'8
                            c'2
                        }
                    }
                }

            **Example 4c.** Sets the preferred denominator of each tuplet to
            ``13``. Setting does not affect any tuplet:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 4)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         ),
                ...     preferred_denominator=13,
                ...     )

            ::

                >>> divisions = [(2, 16), (4, 16), (6, 16), (8, 16)]
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
                        \time 2/16
                        \times 4/5 {
                            c'32 [
                            c'8 ]
                        }
                    }
                    {
                        \time 4/16
                        \times 4/5 {
                            c'16
                            c'4
                        }
                    }
                    {
                        \time 6/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'2
                        }
                    }
                    {
                        \time 8/16
                        \times 4/5 {
                            c'8
                            c'2
                        }
                    }
                }

        Set to ``'divisions'``, duration, positive integer or none.

        Returns ``'divisions'``, duration, positive integer or none.
        '''
        return self._preferred_denominator

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

            This is default behavior.

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

        ..  container:: example

            **Example 3.** Ties across every other division:

            ::

                >>> pattern = rhythmmakertools.BooleanPattern(
                ...     indices=[0],
                ...     period=2,
                ...     )
                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(2, 3), (1, -2, 1)],
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=pattern,
                ...         ),
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                            c'16.
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'8 [
                            c'8. ~ ]
                        }
                    }
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16.
                            r8.
                            c'16.
                        }
                    }
                }

        Set to tie specifier or none.

        Returns tie speicifer or none.
        '''
        return RhythmMaker.tie_specifier.fget(self)

    @property
    def tuplet_ratios(self):
        r'''Gets tuplet ratios of tuplet rhythm-maker.

        ..  container:: example

            **Example 1.** Makes tuplets with ``3:2`` ratios:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, 2)],
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                    {
                        {
                            c'8. [
                            c'8 ]
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Makes tuplets with alternating ``1:-1`` and ``3:1`` 
            ratios:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, -1), (3, 1)],
                ...     )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16), (5, 16)]
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
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'4.
                            c'8
                        }
                    }
                }

        Set to tuple of ratios.

        Returns tuple of ratios.
        '''
        return self._tuplet_ratios

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of tuplet rhythm-maker.

        ..  container:: example

            **Example 1a.** Makes diminished tuplets and does not avoid dots:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=False,
                ...         is_diminution=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 8), (3, 8), (7, 16)]
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
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 7/16
                        {
                            c'8.. [
                            c'8.. ]
                        }
                    }
                }

            This is default behavior.

            **Example 1b.** Makes diminished tuplets and avoids dots:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         is_diminution=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 8), (3, 8), (7, 16)]
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
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4
                            c'4
                        }
                    }
                    {
                        \time 7/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4
                            c'4
                        }
                    }
                }

        ..  container:: example

            **Example 2a.** Makes augmented tuplets and does not avoid dots:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=False,
                ...         is_diminution=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 8), (3, 8), (7, 16)]
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
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8. [
                            c'8. ]
                        }
                    }
                    {
                        \time 7/16
                        {
                            c'8.. [
                            c'8.. ]
                        }
                    }
                }

            **Example 2b.** Makes augmented tuplets and avoids dots:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         is_diminution=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(2, 8), (3, 8), (7, 16)]
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
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            c'8 [
                            c'8 ]
                        }
                    }
                    {
                        \time 7/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 7/4 {
                            c'8 [
                            c'8 ]
                        }
                    }
                }

        ..  container:: example

            **Example 3a.** Generates length-1 tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, -2), (1,), (-2, 3), (1,)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         simplify_tuplets=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
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
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            r4
                        }
                    }
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'2
                        }
                    }
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            r4
                            c'4.
                        }
                    }
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'2
                        }
                    }
                }

            **Example 3b.** Simplifies length-1 tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, -2), (1,), (-2, 3), (1,)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         avoid_dots=True,
                ...         simplify_tuplets=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
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
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            r4
                        }
                    }
                    {
                        {
                            c'4.
                        }
                    }
                    {
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            r4
                            c'4.
                        }
                    }
                    {
                        {
                            c'4.
                        }
                    }
                }

        ..  container:: example

            **Example 4a.** Leaves trivial tuplets enclosed in curly braces in
            LilyPond output:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     tuplet_ratios=[(2, 3), (1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         flatten_trivial_tuplets=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (2, 8), (3, 8), (2, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4
                            c'4. ~
                        }
                    }
                    {
                        \time 2/8
                        {
                            c'8 [
                            c'8 ~ ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4
                            c'4. ~
                        }
                    }
                    {
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                }

            Runs of eighth notes are enclosed in a first set of curly braces
            (representing trivial tuplets) and a second set of curly braces
            (representing measures). This is default behavior.

            **Example 4b.** Flattens trivial tuplets:

            ::

                >>> maker = rhythmmakertools.TupletRhythmMaker(
                ...     tie_specifier=rhythmmakertools.TieSpecifier(
                ...         tie_across_divisions=True,
                ...         ),
                ...     tuplet_ratios=[(2, 3), (1, 1)],
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         flatten_trivial_tuplets=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 8), (2, 8), (3, 8), (2, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4
                            c'4. ~
                        }
                    }
                    {
                        \time 2/8
                        c'8 [
                        c'8 ~ ]
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4
                            c'4. ~
                        }
                    }
                    {
                        \time 2/8
                        c'8 [
                        c'8 ]
                    }
                }

            Runs of eighth notes are now enclosed in only one set of curly
            braces (representing measures). The graphic output of the two
            examples is the same.

            .. note:: Flattening trivial tuplets makes it possible 
                subsequently to rewrite the meter of the untupletted notes.

        Defaults to none.

        Set to tuplet spelling specifier or none.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(TupletRhythmMaker, self)
        return superclass.tuplet_spelling_specifier