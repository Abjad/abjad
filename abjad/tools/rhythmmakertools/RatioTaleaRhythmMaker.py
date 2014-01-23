# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import new


class RatioTaleaRhythmMaker(RhythmMaker):
    r'''Ratio-talea rhythm-maker.

    ..  container:: example

        Makes tuplets with ``3:2`` leaf ratios each.

        ::

            >>> maker = rhythmmakertools.RatioTaleaRhythmMaker(
            ...     ratio_talea=[(3, 2)],
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
                        c'8.
                        c'8
                    }
                }
            }

    ..  container:: example

        Makes tuplets with alternating ``1:-1`` and ``3:1`` leaf ratios.

        ::

            >>> maker = rhythmmakertools.RatioTaleaRhythmMaker(
            ...     ratio_talea=[(1, -1), (3, 1)],
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
                    \times 5/8 {
                        c'4
                        r4
                    }
                }
            }

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_diminution',
        '_ratio_talea',
        )

    _class_name_abbreviation = 'RT'

    _human_readable_class_name = 'ratio-talea rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        ratio_talea=((1, 1), (1, 2), (1, 3)),
        is_diminution=True,
        beam_cells_together=False,
        beam_each_cell=True,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_across_divisions=False,
        ):
        RhythmMaker.__init__(
            self,
            beam_cells_together=beam_cells_together,
            beam_each_cell=beam_each_cell,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_across_divisions=tie_across_divisions,
            )
        ratio_talea = tuple(mathtools.Ratio(x) for x in ratio_talea)
        self._ratio_talea = ratio_talea
        self._is_diminution = is_diminution

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls ratio-talea rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = maker(divisions)
                >>> for division in music:
                ...     division
                FixedDurationTuplet(Duration(1, 2), "c'4 r4")
                FixedDurationTuplet(Duration(3, 8), "c'4. c'8")
                FixedDurationTuplet(Duration(5, 16), "c'4 r4")

        Returns list of selections. Each selection contains exactly one
        fixed-duration tuplet.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats ratio-talea rhythm-maker.

        ..  container:: example

            ::

                rhythmmakertools.RatioTaleaRhythmMaker(
                    ratio_talea=(
                        mathtools.Ratio(1, -1),
                        mathtools.Ratio(3, 1),
                        ),
                    is_diminution=True,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(RatioTaleaRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new ratio-talea rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, is_diminution=False)

            ::

                >>> print format(new_maker)
                rhythmmakertools.RatioTaleaRhythmMaker(
                    ratio_talea=(
                        mathtools.Ratio(1, -1),
                        mathtools.Ratio(3, 1),
                        ),
                    is_diminution=False,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = new_maker(divisions)
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
                            c'4
                            r4
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            c'8.
                            c'16
                        }
                    }
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'8
                            r8
                        }
                    }
                }

        Returns new ratio-talea rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            'is_diminution': self.is_diminution,
            'ratio_talea': self.ratio_talea,
            'tie_across_divisions': self.tie_across_divisions,
            }
        arguments.update(kwargs)
        new_rhythm_maker = type(self)(**arguments)
        return new_rhythm_maker

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        result = []
        if not isinstance(seeds, int):
            seeds = 0
        ratio_talea = datastructuretools.CyclicTuple(
            sequencetools.rotate_sequence(self.ratio_talea, seeds)
            )
        for duration_index, duration_pair in enumerate(duration_pairs):
            ratio = ratio_talea[duration_index]
            duration = durationtools.Duration(duration_pair)
            tuplet = self._make_tuplet(duration, ratio)
            result.append(tuplet)
        return result

    def _make_tuplet(self, duration, ratio):
        tuplet = scoretools.Tuplet.from_duration_and_ratio(
            duration,
            ratio,
            avoid_dots=True,
            is_diminution=self.is_diminution,
            )
        return tuplet

    ### PUBLIC PROPERTIES ###

    @property
    def is_diminution(self):
        r'''Is true when output tuplets should be diminuted.
        False when output tuplets should be augmented.

        ..  container:: example

            ::

                >>> maker.is_diminution
                True

        Returns boolean.
        '''
        return self._is_diminution

    @property
    def ratio_talea(self):
        r'''Gets ratio talea

        ..  container:: example

            ::

                >>> maker.ratio_talea
                (Ratio(1, -1), Ratio(3, 1))

        Returns tuple of ratios.
        '''
        return self._ratio_talea

    @property
    def tie_across_divisions(self):
        r'''Is true when the last and first leaves of adjacent output tuplets
        should be tied together. Otherwise false.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.RatioTaleaRhythmMaker(
                ...     ratio_talea=[(2, 3), (1, -2, 1)],
                ...     tie_across_divisions=True,
                ...     )

            ::

                >>> maker.tie_across_divisions
                True

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
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'8
                            r4
                            c'8 ~
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'8
                            c'8.
                        }
                    }
                }

        Returns boolean.
        '''
        return self._tie_across_divisions

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses ratio-talea rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.RatioTaleaRhythmMaker(
                    ratio_talea=(
                        mathtools.Ratio(1, -2, 1),
                        mathtools.Ratio(3, 2),
                        ),
                    is_diminution=True,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=False,
                    tie_across_divisions=True,
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
                            c'8 ~
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'4.
                            c'4 ~
                        }
                    }
                    {
                        \time 5/16
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'8
                            r4
                            c'8
                        }
                    }
                }

        Defined equal to copy of maker with `ratio_talea` reversed, and each
        ratio in `ratio_talea` reversed.

        Returns new ratio-talea rhythm-maker.
        '''
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        ratio_talea = []
        for ratio in reversed(self.ratio_talea):
            ratio = mathtools.Ratio([x for x in reversed(ratio)])
            ratio_talea.append(ratio)
        ratio_talea = tuple(ratio_talea)
        maker = new(
            self,
            decrease_durations_monotonically=decrease_durations_monotonically,
            ratio_talea=ratio_talea,
            )
        return maker
