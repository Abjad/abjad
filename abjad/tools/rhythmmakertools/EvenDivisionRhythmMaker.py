# -*- encoding: utf-8 -*-
import copy
import math
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach


class EvenDivisionRhythmMaker(RhythmMaker):
    r'''Even division rhythm-maker.

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a list of selections as
    output (structured one selection per input division).
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_denominators',
        '_extra_counts_per_division',
        )

    _human_readable_class_name = 'even division rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        denominators=None,
        extra_counts_per_division=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            )
        assert mathtools.all_are_nonnegative_integer_powers_of_two(
            denominators), repr(denominators)
        denominators = tuple(denominators)
        self._denominators = denominators
        if extra_counts_per_division is not None:
            assert mathtools.all_are_integer_equivalent_exprs(
                extra_counts_per_division), repr(extra_counts_per_division)
            extra_counts_per_division = [
                int(_) for _ in extra_counts_per_division
                ]
            extra_counts_per_division = tuple(extra_counts_per_division)
        self._extra_counts_per_division = extra_counts_per_division

    ### SPECIAL METHODS ###

    def __call__(self, divisions):
        r'''Calls even division rhythm-maker on `divisions`.

        ..  container:: example

                >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16, 16, 8],
                ...     extra_counts_per_division=[1, 0],
                ...     )

            ::

                >>> divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
                >>> selections = maker(divisions)

            ::

                >>> for selection in selections:
                ...     selection
                Selection(FixedDurationTuplet(Duration(3, 8), "c'16 c'16 c'16 c'16 c'16 c'16 c'16"),)
                Selection(FixedDurationTuplet(Duration(1, 2), "c'16 c'16 c'16 c'16 c'16 c'16 c'16 c'16"),)
                Selection(FixedDurationTuplet(Duration(3, 8), "c'8 c'8 c'8 c'8"),)
                Selection(FixedDurationTuplet(Duration(1, 2), "c'16 c'16 c'16 c'16 c'16 c'16 c'16 c'16"),)

            ::

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
                        \time 3/8
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
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
                        \time 4/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        Returns list of of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import rhythmmakertools
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='denominators',
                command='d',
                editor=idetools.getters.get_positive_powers_of_two,
                ),
            systemtools.AttributeDetail(
                name='extra_counts_per_division',
                command='ec',
                editor=idetools.getters.get_integers,
                ),
            systemtools.AttributeDetail(
                name='beam_specifier',
                command='bs',
                editor=rhythmmakertools.BeamSpecifier,
                ),
            systemtools.AttributeDetail(
                name='duration_spelling_specifier',
                command='ds',
                editor=rhythmmakertools.DurationSpellingSpecifier,
                ),
            systemtools.AttributeDetail(
                name='tie_specifier',
                command='ts',
                editor=rhythmmakertools.TieSpecifier,
                ),
            )

    ### PRIVATE METHODS ###

    def _make_music(self, divisions, seeds):
        from abjad.tools import rhythmmakertools
        assert not seeds, repr(seeds)
        selections = []
        divisions = [durationtools.Division(_) for _ in divisions]
        denominators = datastructuretools.CyclicTuple(self.denominators)
        extra_counts_per_division = self.extra_counts_per_division or (0,)
        extra_counts_per_division = datastructuretools.CyclicTuple(
            extra_counts_per_division
            )
        for i, division in enumerate(divisions):
            # not yet extended to work with non-power-of-two divisions
            assert mathtools.is_positive_integer_power_of_two(
                division.denominator), repr(division)
            denominator = denominators[i]
            extra_count = extra_counts_per_division[i]
            basic_duration = durationtools.Duration(1, denominator)
            assert basic_duration <= division, repr((division, basic_duration))
            unprolated_note_count = division / basic_duration
            unprolated_note_count = int(unprolated_note_count)
            unprolated_note_count = unprolated_note_count or 1
            if 0 < extra_count:
                modulus = 2 * unprolated_note_count
                extra_count = extra_count % modulus
            elif extra_count < 0:
                modulus = int(unprolated_note_count / 2.0)
                extra_count = abs(extra_count) % modulus
                extra_count *= -1
            note_count = unprolated_note_count + extra_count
            durations = note_count * [basic_duration]
            notes = scoretools.make_notes([0], durations)
            assert all(
                _.written_duration.denominator == denominator 
                for _ in notes
                )
            tuplet_duration = durationtools.Duration(division)
            tuplet = scoretools.FixedDurationTuplet(
                duration=tuplet_duration,
                music=notes,
                )
            selection = selectiontools.Selection(tuplet)
            selections.append(selection)
        self._apply_beam_specifier(selections)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def denominators(self):
        r'''Gets denominators of rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16, 16, 8],
                ...     )

            ::

                >>> maker.denominators
                (16, 16, 8)

        Returns tuple of nonnegative integer powers of two.
        '''
        return self._denominators

    @property
    def extra_counts_per_division(self):
        r'''Gets extra counts per division of rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16, 16, 8],
                ...     extra_counts_per_division=[1],
                ...     )

            ::

                >>> maker.extra_counts_per_division
                (1,)

        Returns (possibly empty) tuple of integers or none.
        '''
        return self._extra_counts_per_division