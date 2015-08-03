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

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_exponent',
        )

    _class_name_abbreviation = ('RM', 'E')

    _human_readable_class_name = 'even-run rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        exponent=None,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        if exponent is not None:
            assert mathtools.is_nonnegative_integer(exponent)
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        self._exponent = exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
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
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__call__(
            divisions,
            rotation=rotation,
            )

    def __format__(self, format_specification=''):
        r'''Formats even run rhythm-maker.

        ..  container:: example

            ::

                >>> print(format(maker))
                rhythmmakertools.EvenRunRhythmMaker()

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self._get_duration_spelling_specifier()
        forbidden_written_duration = \
            duration_spelling_specifier.forbidden_written_duration
        time_signature = indicatortools.TimeSignature(division)
        implied_prolation = time_signature.implied_prolation
        numerator, denominator = division.pair
        denominator = mathtools.greatest_power_of_two_less_equal(denominator)
        assert mathtools.is_positive_integer_power_of_two(denominator)
        exponent = self.exponent or 0
        denominator_multiplier = 2 ** exponent
        denominator *= denominator_multiplier
        unit_duration = durationtools.Duration(1, denominator)
        if forbidden_written_duration is not None:
            multiplier = 1
            while forbidden_written_duration <= unit_duration:
                unit_duration /= 2
                multiplier *= 2
            numerator *= multiplier
        numerator *= denominator_multiplier
        notes = scoretools.make_notes(numerator * [0], [unit_duration])
        if implied_prolation == 1:
            result = scoretools.Container(notes)
        else:
            multiplier = implied_prolation
            result = scoretools.Tuplet(multiplier, notes)
        return result

    def _make_music(self, divisions, rotation):
        from abjad.tools import rhythmmakertools
        selections = []
        for division in divisions:
            prototype = mathtools.NonreducedFraction
            assert isinstance(division, prototype), division
        for division in divisions:
            container = self._make_container(division)
            selection = selectiontools.Selection(container)
            selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        if beam_specifier.beam_divisions_together:
            durations = []
            for selection in selections:
                duration = selection.get_duration()
                durations.append(duration)
            beam = spannertools.DuratedComplexBeam(
                durations=durations,
                span_beam_count=1,
                nibs_towards_nonbeamable_components=False,
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

        Returns duration spelling specifier or none.
        '''
        return self._duration_spelling_specifier

    @property
    def exponent(self):
        r'''Gets exponent of even-run rhythm-maker.

        ..  container:: example

            **Example 1.** Makes even run of notes with durations
            equal to ``1/(2**0 * d)`` or ``1/d``:

            ::

                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     exponent=0,
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

            (``d`` equals the denominator of each input division.)
            
            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/8``, ``1/4``, ``1/4``.

            This is default behavior.

        ..  container:: example

            **Example 2.** Makes even run of notes with durations
            equal to ``1/(2**1 * d)`` or ``1/(2d)``:

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

            (``d`` equals the denominator of each input division.)

            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/16``, ``1/8``, ``1/8``.

        ..  container:: example

            **Example 3.** Makes even run of notes with durations
            equal to ``1/(2**2 * d)`` or ``1/(4d)``:

            ::

                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     exponent=2,
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
                            c'32 [
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32 ]
                        }
                    }
                    {
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
                    }
                    {
                        \time 2/4
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

            (``d`` equals the denominator of each input division.)

            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/32``, ``1/16``, ``1/16``.

        Defaults to none.
        
        Interprets none equal to ``0``.

        Returns nonnegative integer or none.
        '''
        return self._exponent

    @property
    def tie_specifier(self):
        r'''Gets tie specifier of rhythm-maker.

        ..  container:: example

            **Example 1.** Do not tie across any divisions:

            ::

                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=False,
                ...     )
                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
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
                        \time 5/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    }
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
                        \time 2/8
                        {
                            c'8 [
                            c'8 ]
                        }
                    }
                }

        ..  container:: example

            **Example 2.** Ties across all divisions:

            ::

                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=True,
                ...     )
                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
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
                        \time 5/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ~ ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ~ ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ~ ]
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

        ..  container:: example

            **Example 3.** Ties across every other pair of divisions (starting
            with the first):

            ::

                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=[1, 0],
                ...     )
                >>> maker = rhythmmakertools.EvenRunRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
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
                        \time 5/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8
                            c'8 ~ ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'8 [
                            c'8
                            c'8 ]
                        }
                    }
                    {
                        \time 4/8
                        {
                            c'8 [
                            c'8
                            c'8
                            c'8 ~ ]
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

        Returns boolean.
        '''
        return RhythmMaker.tie_specifier.fget(self)

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of even run rhythm-maker.

        ..  note:: not yet implemented.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.tuplet_spelling_specifier