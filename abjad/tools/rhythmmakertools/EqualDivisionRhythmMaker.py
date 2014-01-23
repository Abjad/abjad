# -*- encoding: utf-8 -*-
import math
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import new


class EqualDivisionRhythmMaker(RhythmMaker):
    r'''Equal division rhythm-maker.

    ..  container:: example

        Makes tuplets with ``4`` equal duration notes each.

        ::

            >>> maker = rhythmmakertools.EqualDivisionRhythmMaker(leaf_count=4)

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
                        c'8 [
                        c'8
                        c'8
                        c'8 ]
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'8 [
                        c'8
                        c'8
                        c'8 ]
                    }
                }
                {
                    \time 5/16
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 5/8 {
                        c'8 [
                        c'8
                        c'8
                        c'8 ]
                    }
                }
            }

    ..  container:: example

        Makes tuplets with ``5`` equal duration notes each.

        ::

            >>> maker = rhythmmakertools.EqualDivisionRhythmMaker(leaf_count=5)

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
                        c'8 [
                        c'8
                        c'8
                        c'8
                        c'8 ]
                    }
                }
                {
                    \time 3/8
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        c'8 [
                        c'8
                        c'8
                        c'8
                        c'8 ]
                    }
                }
                {
                    \time 5/16
                    {
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                }
            }

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_diminution',
        '_leaf_count',
        )

    _class_name_abbreviation = 'ED'

    _human_readable_class_name = 'equal-division rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        leaf_count=1,
        is_diminution=True,
        beam_specifier=None,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_across_divisions=False,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_across_divisions=tie_across_divisions,
            )
        assert mathtools.is_integer_equivalent_expr(leaf_count)
        leaf_count = int(leaf_count)
        self._leaf_count = leaf_count
        self._is_diminution = is_diminution

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls equal-division rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> divisions = [(1, 2), (3, 8), (5, 16)]
                >>> music = maker(divisions)
                >>> for selection in music:
                ...     selection
                FixedDurationTuplet(Duration(1, 2), "c'8 c'8 c'8 c'8 c'8")
                FixedDurationTuplet(Duration(3, 8), "c'8 c'8 c'8 c'8 c'8")
                FixedDurationTuplet(Duration(5, 16), "c'16 c'16 c'16 c'16 c'16")

        Returns list of selections. Each selection contains exactly one
        fixed-duration tuplet.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats equal division rhythm-maker.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.EqualDivisionRhythmMaker(
                    leaf_count=5,
                    is_diminution=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(EqualDivisionRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new equal-division rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, is_diminution=False)

            ::

                >>> print format(new_maker)
                rhythmmakertools.EqualDivisionRhythmMaker(
                    leaf_count=5,
                    is_diminution=False,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

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
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        Returns new equal-division rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_specifier': self.beam_specifier,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            'is_diminution': self.is_diminution,
            'leaf_count': self.leaf_count,
            }
        arguments.update(kwargs)
        new = type(self)(**arguments)
        return new

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        tuplets = []
        beam_specifier = self.beam_specifier
        if not beam_specifier:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        for duration_pair in duration_pairs:
            tuplet = self._make_tuplet(duration_pair)
            if beam_specifier.beam_each_cell:
                beam = spannertools.MultipartBeam()
                attach(beam, tuplet)
            tuplets.append(tuplet)
        return tuplets

    def _make_tuplet(self, division):
        numerator, talea_denominator = division
        division_duration = durationtools.Duration(division)
        ratio = self.leaf_count * [1]
        tuplet = scoretools.Tuplet.from_duration_and_ratio(
            division_duration,
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
    def leaf_count(self):
        r'''Gets number of leaves per division.

        ..  container:: example

            ::

                >>> maker.leaf_count
                5

        Returns positive integer.
        '''
        return self._leaf_count

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses equal-division rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.EqualDivisionRhythmMaker(
                    leaf_count=5,
                    is_diminution=True,
                    decrease_durations_monotonically=False,
                    tie_across_divisions=False,
                    )

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
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 5/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        Returns new equal-division rhythm-maker.
        '''
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        maker = new(
            self,
            decrease_durations_monotonically=decrease_durations_monotonically,
            )
        return maker
