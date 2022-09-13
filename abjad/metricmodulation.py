import typing

from . import _getlib
from . import contributions as _contributions
from . import illustrators as _illustrators
from . import indicators as _indicators
from . import ratio as _ratio
from . import score as _score


class MetricModulation:
    r"""
    Metric modulation.

    ..  container:: example

        With notes:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'8."),
        ...     right_rhythm=abjad.Note("c'4."),
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup \abjad-metric-modulation #3 #1 #2 #1 #'(1 . 1)

    ..  container:: example

        With tuplets:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Tuplet((4, 5), "c'4"),
        ...     right_rhythm=abjad.Note("c'4"),
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup \abjad-metric-modulation-tuplet-lhs #2 #0 #4 #5 #2 #0 #'(1 . 1)

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=abjad.Tuplet((4, 5), "c'4"),
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup \abjad-metric-modulation-tuplet-rhs #2 #0 #2 #0 #4 #5 #'(1 . 1)

    ..  container:: example

        With tuplets again:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c16."),
        ...     right_rhythm=abjad.Tuplet((2, 3), "c8"),
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup \abjad-metric-modulation-tuplet-rhs #4 #1 #3 #0 #2 #3 #'(1 . 1)

    ..  container:: example

        With ties:

        >>> notes = abjad.makers.make_notes([0], [(5, 16)])
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=notes,
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup { \score
                {
                    \context Score = "Score"
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = 0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \context RhythmicStaff = "Rhythmic_Staff"
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = 5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = 4
                            \override TupletBracket.padding = 1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = 0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            c'4
                        }
                    >>
                    \layout
                    {
                        indent = 0
                        ragged-right = ##t
                    }
                }
            =
            \hspace #-0.5
            \score
                {
                    \context Score = "Score"
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = 0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \context RhythmicStaff = "Rhythmic_Staff"
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = 5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = 4
                            \override TupletBracket.padding = 1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = 0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            c'4
                            ~
                            c'16
                        }
                    >>
                    \layout
                    {
                        indent = 0
                        ragged-right = ##t
                    }
                } }

    ..  container:: example

        With ties and tuplets:

        >>> notes = abjad.makers.make_notes([0], [(5, 16)])
        >>> tuplet = abjad.Tuplet((2, 3), notes)
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=tuplet,
        ... )

        >>> lilypond_file = abjad.LilyPondFile(
        ...     [r'\include "abjad.ily"', metric_modulation]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(metric_modulation)
            >>> print(string)
            \markup { \score
                {
                    \context Score = "Score"
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = 0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \context RhythmicStaff = "Rhythmic_Staff"
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = 5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = 4
                            \override TupletBracket.padding = 1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = 0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            c'4
                        }
                    >>
                    \layout
                    {
                        indent = 0
                        ragged-right = ##t
                    }
                }
            =
            \hspace #-0.5
            \score
                {
                    \context Score = "Score"
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = 0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \context RhythmicStaff = "Rhythmic_Staff"
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = 5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = 4
                            \override TupletBracket.padding = 1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = 0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            \tweak edge-height #'(0.7 . 0)
                            \times 2/3
                            {
                                c'4
                                ~
                                c'16
                            }
                        }
                    >>
                    \layout
                    {
                        indent = 0
                        ragged-right = ##t
                    }
                } }


    ..  container:: example

        Attach metric modulations to generate score output:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 e'4 d'4")
        >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0])
        >>> score = abjad.Score([staff])

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c4"),
        ...     right_rhythm=abjad.Note("c8."),
        ... )
        >>> abjad.attach(metric_modulation, staff[3], direction=abjad.UP)
        >>> abjad.override(staff).TextScript.staff_padding = 2.5

        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = 2.5
                }
                {
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    f'4
                    ^ \markup \abjad-metric-modulation #2 #0 #3 #1 #'(1 . 1)
                    e'4
                    d'4
                }
            >>

    """

    __slots__ = (
        "_hide",
        "_left_markup",
        "_left_rhythm",
        "_right_markup",
        "_right_rhythm",
        "_scale",
    )

    directed: typing.ClassVar[bool] = True

    def __init__(
        self,
        left_rhythm,
        right_rhythm,
        *,
        hide: bool = False,
        left_markup: _indicators.Markup = None,
        right_markup: _indicators.Markup = None,
        scale: tuple[int | float, int | float] = (1, 1),
    ) -> None:
        self._hide = bool(hide)
        left_rhythm = self._initialize_rhythm(left_rhythm)
        self._left_rhythm = left_rhythm
        right_rhythm = self._initialize_rhythm(right_rhythm)
        self._right_rhythm = right_rhythm
        self._right_rhythm = right_rhythm
        if left_markup is not None:
            assert isinstance(left_markup, _indicators.Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, _indicators.Markup)
        self._right_markup = right_markup
        assert isinstance(scale, tuple), repr(scale)
        self._scale = scale

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is another metric modulation with the same
        ratio as this metric modulation.

        ..  container:: example

            >>> metric_modulation_1 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ... )
            >>> metric_modulation_2 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ... )
            >>> notes = abjad.makers.make_notes([0], [(5, 16)])
            >>> metric_modulation_3 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=notes,
            ... )

            >>> metric_modulation_1.ratio
            Ratio(numbers=(2, 3))
            >>> metric_modulation_2.ratio
            Ratio(numbers=(2, 3))
            >>> metric_modulation_3.ratio
            Ratio(numbers=(4, 5))

            >>> metric_modulation_1 == metric_modulation_1
            True
            >>> metric_modulation_1 == metric_modulation_2
            True
            >>> metric_modulation_1 == metric_modulation_3
            False

            >>> metric_modulation_2 == metric_modulation_1
            True
            >>> metric_modulation_2 == metric_modulation_2
            True
            >>> metric_modulation_2 == metric_modulation_3
            False

            >>> metric_modulation_3 == metric_modulation_1
            False
            >>> metric_modulation_3 == metric_modulation_2
            False
            >>> metric_modulation_3 == metric_modulation_3
            True

        """
        # custom definition because input rhythms don't compare:
        if isinstance(argument, type(self)):
            if self.ratio == argument.ratio:
                return True
        return False

    def __hash__(self) -> int:
        """
        Hashes metric modulation.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(left_rhythm={self.left_rhythm!r}, right_rhythm={self.right_rhythm!r})"

    ### PRIVATE METHODS ###

    def _get_lilypond_command_string(self):
        if self._note_to_note():
            arguments = self._get_markup_arguments()
            left_exponent, left_dots, right_exponent, right_dots = arguments
            string = r"\abjad-metric-modulation"
            string += f" #{left_exponent} #{left_dots}"
            string += f" #{right_exponent} #{right_dots}"
        elif self._rhs_tuplet():
            arguments = self._get_markup_arguments()
            note_exponent, note_dots = arguments[:2]
            tuplet_exponent, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
            string = r"\abjad-metric-modulation-tuplet-rhs"
            string += f" #{note_exponent} #{note_dots}"
            string += f" #{tuplet_exponent} #{tuplet_dots}"
            string += f" #{tuplet_n} #{tuplet_d}"
        elif self._lhs_tuplet():
            arguments = self._get_markup_arguments()
            tuplet_exponent, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
            note_exponent, note_dots = arguments[4:]
            string = r"\abjad-metric-modulation-tuplet-lhs"
            string += f" #{tuplet_exponent} #{tuplet_dots}"
            string += f" #{tuplet_n} #{tuplet_d}"
            string += f" #{note_exponent} #{note_dots}"
        else:
            return None
        string += f" #'({self.scale[0]} . {self.scale[1]})"
        return string

    def _get_lilypond_format(self):
        markup = self._get_markup()
        return markup.string

    def _get_contributions(self, *, component=None, wrapper=None):
        contributions = _contributions.ContributionsBySite()
        if not self.hide:
            markup = self._get_markup()
            contributions = markup._get_contributions(
                component=component, wrapper=wrapper
            )
        return contributions

    def _get_markup(self):
        string = self._get_lilypond_command_string()
        if string is not None:
            markup = _indicators.Markup(rf"\markup {string}")
            return markup
        strings = []
        string = _illustrators.selection_to_score_markup_string(self.left_rhythm)
        strings.extend(string.split("\n"))
        strings.append("=")
        strings.append(r"\hspace #-0.5")
        string = _illustrators.selection_to_score_markup_string(self.right_rhythm)
        strings.extend(string.split("\n"))
        string = "\n".join(strings)
        string = rf"\markup {{ {string} }}"
        markup = _indicators.Markup(string)
        return markup

    def _get_markup_arguments(self):
        if self._note_to_note():
            left_exponent = self.left_rhythm[0].written_duration.exponent
            left_dots = self.left_rhythm[0].written_duration.dot_count
            right_exponent = self.right_rhythm[0].written_duration.exponent
            right_dots = self.right_rhythm[0].written_duration.dot_count
            return (left_exponent, left_dots, right_exponent, right_dots)
        elif self._lhs_tuplet():
            tuplet_exponent = self.left_rhythm[0][0].written_duration.exponent
            tuplet_dots = self.left_rhythm[0][0].written_duration.dot_count
            tuplet_n = self.left_rhythm[0].multiplier.numerator
            tuplet_d = self.left_rhythm[0].multiplier.denominator
            note_exponent = self.right_rhythm[0].written_duration.exponent
            note_dots = self.right_rhythm[0].written_duration.dot_count
            return (
                tuplet_exponent,
                tuplet_dots,
                tuplet_n,
                tuplet_d,
                note_exponent,
                note_dots,
            )
        elif self._rhs_tuplet():
            note_exponent = self.left_rhythm[0].written_duration.exponent
            note_dots = self.left_rhythm[0].written_duration.dot_count
            tuplet_exponent = self.right_rhythm[0][0].written_duration.exponent
            tuplet_dots = self.right_rhythm[0][0].written_duration.dot_count
            tuplet_n = self.right_rhythm[0].multiplier.numerator
            tuplet_d = self.right_rhythm[0].multiplier.denominator
            return (
                note_exponent,
                note_dots,
                tuplet_exponent,
                tuplet_dots,
                tuplet_n,
                tuplet_d,
            )
        else:
            raise Exception("implement tied note values.")

    def _initialize_rhythm(self, rhythm):
        if isinstance(rhythm, _score.Component):
            selection = [rhythm]
        else:
            selection = rhythm
        return selection

    def _lhs_tuplet(self):
        if (
            isinstance(self.left_rhythm[0], _score.Tuplet)
            and len(self.left_rhythm[0]) == 1
            and isinstance(self.right_rhythm[0], _score.Note)
            and len(self.right_rhythm) == 1
        ):
            return True
        return False

    def _note_to_note(self):
        if (
            isinstance(self.left_rhythm[0], _score.Note)
            and len(self.left_rhythm) == 1
            and isinstance(self.right_rhythm[0], _score.Note)
            and len(self.right_rhythm) == 1
        ):
            return True
        return False

    def _rhs_tuplet(self):
        if (
            isinstance(self.left_rhythm[0], _score.Note)
            and len(self.left_rhythm) == 1
            and isinstance(self.right_rhythm[0], _score.Tuplet)
            and len(self.right_rhythm[0]) == 1
        ):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def hide(self) -> bool:
        """
        Is true when metric modulation generates no LilyPond output.
        """
        return self._hide

    @property
    def left_markup(self) -> _indicators.Markup | None:
        """
        Gets left markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ... )
            >>> metric_modulation.left_markup

        """
        return self._left_markup

    @property
    def left_rhythm(self):
        """
        Gets left rhythm of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ... )
            >>> metric_modulation.left_rhythm
            [Note("c'4")]

        Returns selection.
        """
        return self._left_rhythm

    @property
    def ratio(self) -> _ratio.Ratio:
        """
        Gets ratio of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ... )
            >>> metric_modulation.ratio
            Ratio(numbers=(2, 3))

        """
        left_duration = _getlib._get_duration(self.left_rhythm)
        right_duration = _getlib._get_duration(self.right_rhythm)
        duration = left_duration / right_duration
        ratio = _ratio.Ratio(duration.pair)
        return ratio

    @property
    def right_markup(self) -> _indicators.Markup | None:
        r"""Gets right markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ... )
            >>> metric_modulation.right_markup

        """
        return self._right_markup

    @property
    def right_rhythm(self):
        """
        Gets right tempo of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ... )
            >>> metric_modulation.right_rhythm
            [Note("c'4.")]

        """
        return self._right_rhythm

    @property
    def scale(self) -> tuple[int | float, int | float]:
        r"""
        Gets scale of output markup.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 e'4 d'4")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0])
            >>> score = abjad.Score([staff])

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c4"),
            ...     right_rhythm=abjad.Note("c8."),
            ...     scale=(0.5, 0.5),
            ... )
            >>> abjad.attach(metric_modulation, staff[3], direction=abjad.UP)
            >>> abjad.override(staff).TextScript.staff_padding = 2.5

            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = 2.5
                    }
                    {
                        \time 3/4
                        c'4
                        d'4
                        e'4
                        f'4
                        ^ \markup \abjad-metric-modulation #2 #0 #3 #1 #'(0.5 . 0.5)
                        e'4
                        d'4
                    }
                >>

        """
        return self._scale

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on metric modulation.
        """
        pass
