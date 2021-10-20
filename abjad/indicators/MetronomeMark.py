import collections
import dataclasses
import functools
import math
import typing

import quicktions

from .. import bundle as _bundle
from .. import duration as _duration
from .. import enumerate as _enumerate
from .. import markups as _markups
from .. import math as _math
from .. import ratio as _ratio
from .. import sequence as _sequence
from .. import typings as _typings


@functools.total_ordering
@dataclasses.dataclass(unsafe_hash=True)
class MetronomeMark:
    r"""
    MetronomeMark.

    ..  container:: example

        Initializes integer-valued metronome mark:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo 4=90
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Initializes rational-valued metronome mark:

        >>> import quicktions
        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), quicktions.Fraction(272, 3))
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"90" #"2" #"3"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

        Overrides rational-valued metronome mark with decimal string:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ...     decimal="90.66",
        ... )
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.66"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

        Overrides rational-valued metronome mark with exact decimal:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(901, 10),
        ...     decimal=True,
        ... )
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.1"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Initializes from text, duration and range:

        >>> score = abjad.Score()
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), (120, 133), 'Quick')
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo Quick 4=120-133
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Custom markup:

        >>> import quicktions
        >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
        ...     abjad.Duration(1, 4),
        ...     67.5,
        ...  )
        >>> mark = abjad.MetronomeMark(
        ...     reference_duration=(1, 4),
        ...     units_per_minute=quicktions.Fraction(135, 2),
        ...     custom_markup=markup,
        ...  )
        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> score = abjad.Score([staff])
        >>> abjad.attach(mark, staff[0])
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', score])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup \abjad-metronome-mark-markup #2 #0 #1 #"67.5"
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    ..  container:: example

        Decimal overrides:

        >>> import quicktions
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ... )
        >>> mark.decimal is None
        True

        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(272, 3),
        ...     decimal="90.66",
        ... )
        >>> mark.decimal
        '90.66'

        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     quicktions.Fraction(901, 10),
        ...     decimal=True,
        ... )
        >>> mark.decimal
        True

    ..  container:: example

        Set ``hide=True`` when metronome mark should not appear in output (but
        should still determine effective metronome mark):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> metronome_mark_1 = abjad.MetronomeMark((1, 4), 72)
        >>> abjad.attach(metronome_mark_1, staff[0])
        >>> metronome_mark_2 = abjad.MetronomeMark(
        ...     textual_indication='Allegro',
        ...     hide=True,
        ... )
        >>> abjad.attach(metronome_mark_2, staff[2])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                \tempo 4=72
                c'4
                d'4
                e'4
                f'4
            }
        >>

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     prototype = abjad.MetronomeMark
        ...     leaf, abjad.get.effective(leaf, prototype)
        ...
        (Note("c'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72, textual_indication=None, custom_markup=None, decimal=None, hide=False))
        (Note("d'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72, textual_indication=None, custom_markup=None, decimal=None, hide=False))
        (Note("e'4"), MetronomeMark(reference_duration=None, units_per_minute=None, textual_indication='Allegro', custom_markup=None, decimal=None, hide=True))
        (Note("f'4"), MetronomeMark(reference_duration=None, units_per_minute=None, textual_indication='Allegro', custom_markup=None, decimal=None, hide=True))

    """

    reference_duration: typing.Optional[_typings.DurationTyping] = None
    units_per_minute: typing.Union[int, quicktions.Fraction] = None
    textual_indication: typing.Optional[str] = None
    custom_markup: typing.Optional[_markups.Markup] = None
    decimal: typing.Union[bool, str, None] = None
    hide: bool = False

    _is_dataclass = True

    context = "Score"
    parameter = "METRONOME_MARK"
    persistent = True

    _format_slot = "opening"

    _mutates_offsets_in_seconds = True

    def __post_init__(self):
        assert isinstance(self.textual_indication, (str, type(None)))
        if self.reference_duration:
            self.reference_duration = _duration.Duration(self.reference_duration)
        if isinstance(self.units_per_minute, float):
            raise Exception(
                f"do not set units-per-minute to float ({self.units_per_minute});"
                " use fraction with decimal override instead."
            )
        prototype = (int, quicktions.Fraction, collections.abc.Sequence, type(None))
        assert isinstance(self.units_per_minute, prototype)
        if isinstance(self.units_per_minute, collections.abc.Sequence):
            assert len(self.units_per_minute) == 2
            item_prototype = (int, _duration.Duration)
            assert all(isinstance(_, item_prototype) for _ in self.units_per_minute)
            self.units_per_minute = tuple(sorted(self.units_per_minute))
        if self.custom_markup is not None:
            assert isinstance(self.custom_markup, _markups.Markup)
        if self.decimal is not None:
            assert isinstance(self.decimal, (bool, str)), repr(self.decimal)
        assert isinstance(self.hide, bool), repr(self.hide)

    def __eq__(self, argument) -> bool:
        """
        Is true when metronome mark equals ``argument``.

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52)
            >>> mark_2 = abjad.MetronomeMark((3, 32), 52)

            >>> mark_1 == mark_2
            True

            >>> mark_2 == mark_1
            True

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52)
            >>> mark_2 = abjad.MetronomeMark((6, 32), 104)

            >>> mark_1 == mark_2
            False

            >>> mark_2 == mark_1
            False

        ..  container:: example

            >>> mark_1 = abjad.MetronomeMark((3, 32), 52, 'Langsam')
            >>> mark_2 = abjad.MetronomeMark((3, 32), 52, 'Langsam')
            >>> mark_3 = abjad.MetronomeMark((3, 32), 52, 'Slow')

            >>> mark_1 == mark_2
            True

            >>> mark_1 == mark_3
            False

        """
        if not isinstance(argument, type(self)):
            return False
        # 'hide' is excluded from equality testing:
        if (
            self.reference_duration == argument.reference_duration
            and self.units_per_minute == argument.units_per_minute
            and self.textual_indication == argument.textual_indication
            and self.custom_markup == argument.custom_markup
        ):
            return True
        return False

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a metronome mark with quarters per minute greater
        than that of this metronome mark.
        """
        assert isinstance(argument, type(self)), repr(argument)
        self_quarters_per_minute = self.quarters_per_minute or 0
        argument_quarters_per_minute = argument.quarters_per_minute or 0
        assert isinstance(self_quarters_per_minute, (int, float, quicktions.Fraction))
        assert isinstance(
            argument_quarters_per_minute, (int, float, quicktions.Fraction)
        )
        return self_quarters_per_minute < argument_quarters_per_minute

    def __str__(self) -> str:
        """
        Gets string representation of metronome mark.

        ..  container:: example

            Integer-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> str(mark)
            '4=90'

        ..  container:: example

            Rational-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), (272, 3))
            >>> str(mark)
            '4=3-272'

        """
        if self.textual_indication is not None:
            string = self.textual_indication
        elif isinstance(self.units_per_minute, (int, float)):
            string = f"{self._dotted}={self.units_per_minute}"
        elif isinstance(
            self.units_per_minute, quicktions.Fraction
        ) and not _math.is_integer_equivalent_number(self.units_per_minute):
            integer_part = int(float(self.units_per_minute))
            remainder = self.units_per_minute - integer_part
            remainder = quicktions.Fraction(remainder)
            string = f"{self._dotted}={integer_part}+{remainder}"
        elif isinstance(
            self.units_per_minute, quicktions.Fraction
        ) and _math.is_integer_equivalent_number(self.units_per_minute):
            integer = int(float(self.units_per_minute))
            string = f"{self._dotted}={integer}"
        elif isinstance(self.units_per_minute, tuple):
            first = self.units_per_minute[0]
            second = self.units_per_minute[1]
            string = f"{self._dotted}={first}-{second}"
        else:
            raise TypeError(f"unknown: {self.units_per_minute!r}.")
        return string

    @property
    def _dotted(self):
        return self.reference_duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.reference_duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            first, second = self.units_per_minute
            string = f"{self._dotted}={first}-{second}"
            return string
        elif isinstance(self.units_per_minute, quicktions.Fraction):
            markup = MetronomeMark.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                decimal=self.decimal,
            )
            string = str(markup)
            return string
        string = f"{self._dotted}={self.units_per_minute}"
        return string

    def _get_lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = self.textual_indication
            assert isinstance(text, str)
            if " " in text:
                text = f'"{text}"'
        if self.reference_duration is not None and self.units_per_minute is not None:
            equation = self._equation
        if self.custom_markup is not None:
            return rf"\tempo {self.custom_markup}"
        elif text and equation:
            return rf"\tempo {text} {equation}"
        elif equation:
            return rf"\tempo {equation}"
        elif text:
            return rf"\tempo {text}"
        else:
            return r"\tempo \default"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if not self.hide:
            bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    def _get_markup(self):
        if self.custom_markup is not None:
            return self.custom_markup
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        stem_height = 1
        string = "abjad-metronome-mark-markup"
        string += f" #{duration_log}"
        string += f" #{self.reference_duration.dot_count}"
        string += f" #{stem_height}"
        string += f' #"{self.units_per_minute}"'
        markup = _markups.Markup(rf"\markup {string}")
        return markup

    # TODO: refactor to return dict
    def _get_markup_arguments(self):
        assert self.custom_markup is None
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        dot_count = self.reference_duration.dot_count
        stem_height = 1
        if not self.decimal:
            return (
                duration_log,
                dot_count,
                stem_height,
                self.units_per_minute,
            )
        if isinstance(self.decimal, str):
            return (duration_log, dot_count, stem_height, self.decimal)
        assert self.decimal is True, repr(self.decimal)
        # TODO: add abjad.NonreducedFraction.mixed_number property
        fraction = _duration.NonreducedFraction(self.units_per_minute)
        n, d = fraction.pair
        base = n // d
        n = n % d
        return (duration_log, dot_count, stem_height, base, n, d)

    #    @property
    #    def custom_markup(self) -> typing.Optional[_markups.Markup]:
    #        """
    #        """
    #        return self._custom_markup

    #    @property
    #    def decimal(self) -> typing.Union[bool, str, None]:
    #        """
    #        Gets decimal override.
    #        """
    #        return self._decimal

    #    @property
    #    def hide(self) -> typing.Optional[bool]:
    #        r"""
    #        """
    #        return self._hide

    @property
    def is_imprecise(self) -> bool:
        """
        Is true if metronome mark is entirely textual or if metronome mark's
        units_per_minute is a range.

        ..  container:: example

            Imprecise metronome marks:

            >>> abjad.MetronomeMark((1, 4), 60).is_imprecise
            False
            >>> abjad.MetronomeMark(4, 60, 'Langsam').is_imprecise
            False
            >>> abjad.MetronomeMark(textual_indication='Langsam').is_imprecise
            True
            >>> abjad.MetronomeMark(4, (35, 50), 'Langsam').is_imprecise
            True
            >>> abjad.MetronomeMark((1, 4), (35, 50)).is_imprecise
            True

        ..  container:: example

            Precise metronome marks:

            >>> abjad.MetronomeMark((1, 4), 60).is_imprecise
            False

        """
        if self.reference_duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def quarters_per_minute(self) -> typing.Union[tuple, None, quicktions.Fraction]:
        """
        Gets metronome mark quarters per minute.

        ..  container:: example

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.quarters_per_minute
            Fraction(104, 1)

        Gives tuple when metronome mark ``units_per_minute`` is a range.

        Gives none when metronome mark is imprecise.

        Gives fraction otherwise.
        """
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = (
                _duration.Duration(1, 4)
                / self.reference_duration
                * self.units_per_minute[0]
            )
            high = (
                _duration.Duration(1, 4)
                / self.reference_duration
                * self.units_per_minute[1]
            )
            return (low, high)
        result = (
            _duration.Duration(1, 4) / self.reference_duration * self.units_per_minute
        )
        return quicktions.Fraction(result)

    #    @property
    #    def reference_duration(self) -> typing.Optional[_duration.Duration]:
    #        """
    #        Gets reference duration of metronome mark.
    #
    #        ..  container:: example
    #
    #            >>> mark = abjad.MetronomeMark((1, 8), 52)
    #            >>> mark.reference_duration
    #            Duration(1, 8)
    #
    #        """
    #        return self._reference_duration

    #    @property
    #    def textual_indication(self) -> typing.Optional[str]:
    #        """
    #        Gets optional textual indication of metronome mark.
    #
    #        ..  container:: example
    #
    #            >>> mark = abjad.MetronomeMark((1, 8), 52)
    #            >>> mark.textual_indication is None
    #            True
    #
    #        """
    #        return self._textual_indication

    #    @property
    #    def units_per_minute(self) -> typing.Union[int, quicktions.Fraction, None]:
    #        """
    #        Gets units per minute of metronome mark.
    #
    #        ..  container:: example
    #
    #            Integer-valued metronome mark:
    #
    #            >>> mark = abjad.MetronomeMark((1, 4), 90)
    #            >>> mark.units_per_minute
    #            90
    #
    #        ..  container:: example
    #
    #            Rational-valued metronome mark:
    #
    #            >>> import quicktions
    #            >>> mark = abjad.MetronomeMark((1, 4), quicktions.Fraction(272, 3))
    #            >>> mark.units_per_minute
    #            Fraction(272, 3)
    #
    #        """
    #        return self._units_per_minute

    def duration_to_milliseconds(self, duration) -> _duration.Duration:
        """
        Gets millisecond value of ``duration`` under a given metronome mark.

        ..  container:: example

            Dotted sixteenth lasts 1500 msec at quarter equals 60:

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> mark.duration_to_milliseconds((3, 8))
            Duration(1500, 1)

        """
        assert isinstance(self.reference_duration, _duration.Duration)
        denominator = self.reference_duration.denominator
        numerator = self.reference_duration.numerator
        whole_note_duration = 1000
        whole_note_duration *= _duration.Multiplier(denominator, numerator)
        whole_note_duration *= _duration.Multiplier(60, self.units_per_minute)
        duration = _duration.Duration(duration)
        return _duration.Duration(duration * whole_note_duration)

    def list_related_tempos(
        self,
        maximum_numerator=None,
        maximum_denominator=None,
        integer_tempos_only=False,
    ) -> typing.List[typing.Tuple["MetronomeMark", "_ratio.Ratio"]]:
        r"""
        Lists related tempos.

        ..  container:: example

            Rewrites tempo ``4=58`` by ratios ``n:d`` such that ``1 <= n <= 8`` and ``1
            <= d <= 8``.

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=8,
            ...     maximum_denominator=8,
            ...  )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}    {ratio!s}'
            ...     print(string)
            4=29    1:2
            4=33+1/7    4:7
            4=34+4/5    3:5
            4=36+1/4    5:8
            4=38+2/3    2:3
            4=41+3/7    5:7
            4=43+1/2    3:4
            4=46+2/5    4:5
            4=48+1/3    5:6
            4=49+5/7    6:7
            4=50+3/4    7:8
            4=58    1:1
            4=66+2/7    8:7
            4=67+2/3    7:6
            4=69+3/5    6:5
            4=72+1/2    5:4
            4=77+1/3    4:3
            4=81+1/5    7:5
            4=87    3:2
            4=92+4/5    8:5
            4=96+2/3    5:3
            4=101+1/2    7:4
            4=116    2:1

        ..  container:: example

            Integer-valued tempos only:

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=16,
            ...     maximum_denominator=16,
            ...     integer_tempos_only=True,
            ...  )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}    {ratio!s}'
            ...     print(string)
            4=29    1:2
            4=58    1:1
            4=87    3:2
            4=116    2:1

        Constrains ratios such that ``1:2 <= n:d <= 2:1``.
        """
        allowable_numerators = range(1, maximum_numerator + 1)
        allowable_denominators = range(1, maximum_denominator + 1)
        numbers = [allowable_numerators, allowable_denominators]
        pairs = _enumerate.outer_product(numbers)
        multipliers = [_duration.Multiplier(_) for _ in pairs]
        multipliers = [
            _
            for _ in multipliers
            if quicktions.Fraction(1, 2) <= _ <= quicktions.Fraction(2)
        ]
        multipliers.sort()
        multipliers_ = _sequence.Sequence(multipliers).remove_repeats()
        pairs = []
        for multiplier in multipliers_:
            new_units_per_minute = multiplier * self.units_per_minute
            if integer_tempos_only and not _math.is_integer_equivalent_number(
                new_units_per_minute
            ):
                continue
            metronome_mark = type(self)(
                reference_duration=self.reference_duration,
                units_per_minute=new_units_per_minute,
            )
            ratio = _ratio.Ratio(multiplier.pair)
            pair = (metronome_mark, ratio)
            pairs.append(pair)
        return pairs

    @staticmethod
    def make_tempo_equation_markup(
        reference_duration, units_per_minute, *, decimal=None
    ) -> _markups.Markup:
        r"""
        Makes tempo equation markup.

        ..  container:: example

            Integer-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup((1, 4),  90)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-markup #2 #0 #1 #"90"

        ..  container:: example

            Float-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup((1, 4), 90.1)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-markup #2 #0 #1 #"90.1"

        ..  container:: example

            Rational-valued metronome mark:

            >>> import quicktions
            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     abjad.Duration(1, 4),
            ...     quicktions.Fraction(272, 3),
            ... )
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', markup])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"90" #"2" #"3"

        """
        reference_duration_ = _duration.Duration(reference_duration)
        log = reference_duration_.exponent
        dots = reference_duration_.dot_count
        stem = 1
        if isinstance(
            units_per_minute, quicktions.Fraction
        ) and not _math.is_integer_equivalent_number(units_per_minute):
            if decimal:
                decimal_: typing.Union[float, str]
                if decimal is True:
                    decimal_ = float(units_per_minute)
                else:
                    assert isinstance(decimal, str), repr(decimal)
                    decimal_ = decimal
                markup = _markups.Markup(
                    r"\markup \abjad-metronome-mark-markup"
                    f' #{log} #{dots} #{stem} #"{decimal_}"'
                )
            else:
                nonreduced = _duration.NonreducedFraction(units_per_minute)
                base = int(nonreduced)
                remainder = nonreduced - base
                n, d = remainder.pair
                markup = _markups.Markup(
                    r"\markup \abjad-metronome-mark-mixed-number-markup"
                    f" #{log} #{dots} #{stem}"
                    f' #"{base}" #"{n}" #"{d}"'
                )
        else:
            markup = _markups.Markup(
                r"\markup \abjad-metronome-mark-markup"
                f' #{log} #{dots} #{stem} #"{units_per_minute}"'
            )
        return markup
