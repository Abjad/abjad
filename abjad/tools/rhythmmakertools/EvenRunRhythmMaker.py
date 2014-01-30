# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import systemtools
from abjad.tools.rhythmmakertools.BeamSpecifier import BeamSpecifier
from abjad.tools.rhythmmakertools.ExampleWrapper import ExampleWrapper
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.rhythmmakertools.TieSpecifier import TieSpecifier
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class EvenRunRhythmMaker(RhythmMaker):
    r'''Even run rhythm-maker.

    ..  container:: example

        Makes even run of notes each equal in duration to ``1/d``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker()

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                    {
                        c'8 [
                        c'8
                        c'8
                        c'8 ]
                    }
                }
                {
                    \time 3/4
                    {
                        c'4
                        c'4
                        c'4
                    }
                }
                {
                    \time 2/4
                    {
                        c'4
                        c'4
                    }
                }
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_exponent',
        )

    _class_name_abbreviation = 'ER'

    _human_readable_class_name = 'even-run rhythm-maker'

    ### GALLERY INPUT ###

    _gallery_division_lists = (
        [
            (4, 16), (5, 16), (1, 2), (2, 12),
            (1, 2), (2, 12), (4, 16), (5, 16),
        ],
        [
            (1, 11), (3, 8), (3, 8), (3, 8),
            (3, 8), (3, 8), (1, 11), (3, 8),
        ],
        [
            (3, 15), (3, 15), (3, 16),
            (5, 24), (5, 24), (5, 16), 
            (2, 12), (2, 12), (2, 8),
            (3, 28), (3, 28), (3, 16),
            (1, 9), (1, 9), (1, 8),
        ],
        [
            (9, 16), (1, 5), (9, 16),
            (1, 5), (9, 16), (9, 16),
        ],
        )

    _gallery_input_blocks = (
        ExampleWrapper(
            arguments={
                },
            division_lists=_gallery_division_lists,
            ),
        ExampleWrapper(
            arguments={
                'beam_specifier': BeamSpecifier(
                    beam_divisions_together=True,
                    ),
                },
            division_lists=_gallery_division_lists,
            ),
        ExampleWrapper(
            arguments={
                'beam_specifier': BeamSpecifier(
                    beam_each_division=False,
                    ),
                },
            division_lists=_gallery_division_lists,
            ),
        ExampleWrapper(
            arguments={
                'tie_specifier': TieSpecifier(
                    tie_across_divisions=True,
                    ),
                },
            division_lists=_gallery_division_lists,
            ),
        ExampleWrapper(
            arguments={
                'exponent': 1,
                },
            division_lists=_gallery_division_lists,
            ),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        exponent=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        ):
        if exponent is not None:
            assert mathtools.is_nonnegative_integer(exponent)
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            )
        self._exponent = exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls even-run rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.EvenRunRhythmMaker()
                >>> divisions = [(4, 8), (3, 4), (2, 4)]
                >>> result = maker(divisions)
                >>> for selection in result:
                ...     selection
                Selection(Container("c'8 c'8 c'8 c'8"),)
                Selection(Container("c'4 c'4 c'4"),)
                Selection(Container("c'4 c'4"),)

        Returns a list of selections. Each selection holds a single container
        filled with notes.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats even run rhythm-maker.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.EvenRunRhythmMaker()

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new even-run rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, exponent=1)

            ::

                >>> print format(new_maker)
                rhythmmakertools.EvenRunRhythmMaker(
                    exponent=1,
                    )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }
                    {
                        \time 2/4
                        {
                            c'4
                            c'4
                        }
                    }
                }

        Returns new even-run rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        numerator, denominator = division
        time_signature = indicatortools.TimeSignature(division)
        implied_prolation = time_signature.implied_prolation
        denominator = mathtools.greatest_power_of_two_less_equal(denominator)
        assert mathtools.is_positive_integer_power_of_two(denominator)
        exponent = self.exponent or 0
        denominator_multiplier = 2 ** exponent
        denominator *= denominator_multiplier
        unit_duration = durationtools.Duration(1, denominator)
        numerator *= denominator_multiplier
        notes = scoretools.make_notes(numerator * [0], [unit_duration])
        if implied_prolation == 1:
            result = scoretools.Container(notes)
        else:
            multiplier = implied_prolation
            result = scoretools.Tuplet(multiplier, notes)
        return result

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        selections = []
        beam_specifier = self.beam_specifier
        if not beam_specifier:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        for duration_pair in duration_pairs:
            container = self._make_container(duration_pair)
            selection = selectiontools.Selection(container)
            selections.append(selection)
        if beam_specifier.beam_divisions_together:
            durations = []
            for selection in selections:
                duration = selection.get_duration()
                durations.append(duration)
            beam = spannertools.DuratedComplexBeam(
                durations=durations,
                span_beam_count=1,
                nibs_towards_nonbeamable_components=True,
                )
            components = []
            for selection in selections:
                components.extend(selection)
            attach(beam, components)
        elif beam_specifier.beam_each_division:
            for selection in selections:
                beam = spannertools.MultipartBeam()
                attach(beam, selection)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of even-run rhythm-maker.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier(
                ...     forbidden_written_duration=Duration(1, 4),
                ...     )
                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     duration_spelling_specifier=specifier,
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }
                    {
                        \time 2/4
                        {
                            c'4
                            c'4
                        }
                    }
                }

            ..  todo:: make this example work: should forbid quarter notes.

        Returns duration spelling specifier or none.
        '''
        return self._duration_spelling_specifier

    @property
    def exponent(self):
        r'''Gets exponent of even-run rhythm-maker.

        ..  container:: example

            Makes even run of notes each equal in duration to
            ``1/(2**d)`` with ``d`` equal to the denominator of each division
            on which the rhythm-maker is called:

            ::

                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     exponent=1,
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                        \time 3/4
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 2/4
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                }

        Defaults to none and interprets none equal to ``0``.

        Returns nonnegative integer or none.
        '''
        return self._exponent

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of rhythm-maker.

        ..  container:: example

            Ties across divisions:

            ::
            
                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=True,
                ...     )
                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ] ~
                        }
                    }
                    {
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4 ~
                        }
                    }
                    {
                        \time 2/4
                        {
                            c'4
                            c'4
                        }
                    }
                }

        Returns boolean.
        '''
        return RhythmMaker.tie_specifier.fget(self)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses even-run rhythm-maker.

        ..  container:: example
        
            ::

                >>> maker = rhythmmakertools.EvenRunRhythmMaker()
                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.EvenRunRhythmMaker(
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
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
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }
                    {
                        \time 2/4
                        {
                            c'4
                            c'4
                        }
                    }
                }

        Returns new even-run rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self.duration_spelling_specifier
        if duration_spelling_specifier is None:
            default = rhythmmakertools.DurationSpellingSpecifier()
            duration_spelling_specifier = default
        duration_spelling_specifier = duration_spelling_specifier.reverse()
        maker = new(
            self,
            duration_spelling_specifier=duration_spelling_specifier,
            )
        return maker
