from .RhythmMaker import RhythmMaker


class EvenRunRhythmMaker(RhythmMaker):
    r"""
    Even run rhythm-maker.

    ..  container:: example

        Makes even run of notes each equal in duration to ``1/d``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker()

        >>> divisions = [(4, 8), (3, 4), (2, 4)]
        >>> selections = rhythm_maker(divisions)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     selections,
        ...     divisions,
        ...     )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new RhythmicStaff
            {
                {   % measure
                    \time 4/8
                    {
                        c'8
                        [
                        c'8
                        c'8
                        c'8
                        ]
                    }
                }   % measure
                {   % measure
                    \time 3/4
                    {
                        c'4
                        c'4
                        c'4
                    }
                }   % measure
                {   % measure
                    \time 2/4
                    {
                        c'4
                        c'4
                    }
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = (
        '_exponent',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        beam_specifier=None,
        duration_specifier=None,
        exponent=None,
        tie_specifier=None,
        tuplet_specifier=None,
        ):
        import abjad
        if exponent is not None:
            assert abjad.mathtools.is_nonnegative_integer(exponent)
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        self._exponent = exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, previous_state=None):
        """
        Calls even-run rhythm-maker on ``divisions``.

        ..  container:: example

            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker()
            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> result = rhythm_maker(divisions)
            >>> for selection in result:
            ...     selection
            Selection([Container("c'8 c'8 c'8 c'8")])
            Selection([Container("c'4 c'4 c'4")])
            Selection([Container("c'4 c'4")])

        Returns a list of selections. Each selection holds a single container
        filled with notes.
        """
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__call__(divisions, previous_state=previous_state)

    def __format__(self, format_specification=''):
        """
        Formats even run rhythm-maker.

        ..  container:: example

            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker()
            >>> abjad.f(rhythm_maker)
            abjad.rmakers.EvenRunRhythmMaker()

        Returns string.
        """
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        import abjad
        duration_specifier = self._get_duration_specifier()
        forbidden_duration = \
            duration_specifier.forbidden_duration
        time_signature = abjad.TimeSignature(division)
        implied_prolation = time_signature.implied_prolation
        numerator, denominator = division.pair
        denominator = abjad.mathtools.greatest_power_of_two_less_equal(
            denominator)
        assert abjad.mathtools.is_positive_integer_power_of_two(denominator)
        exponent = self.exponent or 0
        denominator_multiplier = 2 ** exponent
        denominator *= denominator_multiplier
        unit_duration = abjad.Duration(1, denominator)
        if forbidden_duration is not None:
            multiplier = 1
            while forbidden_duration <= unit_duration:
                unit_duration /= 2
                multiplier *= 2
            numerator *= multiplier
        numerator *= denominator_multiplier
        maker = abjad.NoteMaker()
        notes = maker(numerator * [0], [unit_duration])
        if implied_prolation == 1:
            result = abjad.Container(notes)
        else:
            multiplier = implied_prolation
            result = abjad.Tuplet(multiplier, notes)
        return result

    def _make_music(self, divisions):
        import abjad
        selections = []
        for division in divisions:
            prototype = abjad.NonreducedFraction
            assert isinstance(division, prototype), division
        for division in divisions:
            container = self._make_container(division)
            selection = abjad.select(container)
            selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        if beam_specifier.beam_divisions_together:
            durations = []
            for selection in selections:
                duration = selection.get_duration()
                durations.append(duration)
            beam = abjad.DuratedComplexBeam(
                durations=durations,
                span_beam_count=1,
                nibs_towards_nonbeamable_components=False,
                )
            components = []
            for selection in selections:
                components.extend(selection)
            leaves = abjad.select(components).leaves()
            abjad.attach(beam, leaves)
        elif beam_specifier.beam_each_division:
            for selection in selections:
                beam = abjad.MultipartBeam()
                leaves = abjad.select(selection).leaves()
                abjad.attach(beam, leaves)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def duration_specifier(self):
        r"""
        Gets duration specifier.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier(
            ...     forbidden_duration=(1, 4),
            ...     )
            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     duration_specifier=specifier,
            ...     )

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/4
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/4
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

        Returns duration specifier or none.
        """
        return self._duration_specifier

    @property
    def exponent(self):
        r"""
        Gets exponent.

        ..  container:: example

            Makes even run of notes with durations equal to ``1/(2**0 * d)`` or
            ``1/d``:

            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     exponent=0,
            ...     )

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/4
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }   % measure
                    {   % measure
                        \time 2/4
                        {
                            c'4
                            c'4
                        }
                    }   % measure
                }

            (``d`` equals the denominator of each input division.)

            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/8``, ``1/4``, ``1/4``.

        ..  container:: example

            Makes even run of notes with durations equal to ``1/(2**1 * d)`` or
            ``1/(2d)``:

            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     exponent=1,
            ...     )

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        {
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/4
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/4
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                }

            (``d`` equals the denominator of each input division.)

            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/16``, ``1/8``, ``1/8``.

        ..  container:: example

            Makes even run of notes with durations equal to ``1/(2**2 * d)`` or
            ``1/(4d)``:

            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     exponent=2,
            ...     )

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 4/8
                        {
                            c'32
                            [
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
                            c'32
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/4
                        {
                            c'16
                            [
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
                            c'16
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/4
                        {
                            c'16
                            [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            ]
                        }
                    }   % measure
                }

            (``d`` equals the denominator of each input division.)

            Input division denominators ``8``, ``4``, ``4`` result in notes
            with durations ``1/32``, ``1/16``, ``1/16``.

        Defaults to none.

        Interprets none equal to ``0``.

        Returns nonnegative integer or none.
        """
        return self._exponent

    @property
    def tie_specifier(self):
        r"""
        Gets tie specifier.

        ..  container:: example

            Do not tie across any divisions:

            >>> tie_specifier = abjad.rmakers.TieSpecifier(
            ...     tie_across_divisions=False,
            ...     )
            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     tie_specifier=tie_specifier,
            ...     )

            >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 5/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/8
                        {
                            c'8
                            [
                            c'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Ties across all divisions:

            >>> tie_specifier = abjad.rmakers.TieSpecifier(
            ...     tie_across_divisions=True,
            ...     )
            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     tie_specifier=tie_specifier,
            ...     )

            >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 5/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/8
                        {
                            c'8
                            [
                            c'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Ties across every other pair of divisions (starting with the
            first):

            >>> tie_specifier = abjad.rmakers.TieSpecifier(
            ...     tie_across_divisions=[1, 0],
            ...     )
            >>> rhythm_maker = abjad.rmakers.EvenRunRhythmMaker(
            ...     tie_specifier=tie_specifier,
            ...     )

            >>> divisions = [(5, 8), (3, 8), (4, 8), (2, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new RhythmicStaff
                {
                    {   % measure
                        \time 5/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 3/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 4/8
                        {
                            c'8
                            [
                            c'8
                            c'8
                            c'8
                            ~
                            ]
                        }
                    }   % measure
                    {   % measure
                        \time 2/8
                        {
                            c'8
                            [
                            c'8
                            ]
                        }
                    }   % measure
                }

        Returns true or false.
        """
        return RhythmMaker.tie_specifier.fget(self)

    @property
    def tuplet_specifier(self):
        r"""
        Gets tuplet specifier.

        ..  note:: not yet implemented.

        Returns tuplet specifier or none.
        """
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.tuplet_specifier
