import collections
from fractions import Fraction
try:
    from quicktions import Fraction # type: ignore
except ImportError:
    pass
import functools
import math
import typing
from abjad import enums
from abjad import exceptions
from abjad import mathtools
from abjad import typings
from abjad.markups import Markup
from abjad.markups import MarkupCommand
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.mathtools.Ratio import Ratio
from abjad.scheme import Scheme
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.new import new
from abjad.top.sequence import sequence
from abjad.utilities.Duration import Duration
from abjad.utilities.Enumerator import Enumerator
from abjad.utilities.Multiplier import Multiplier
from .LilyPondLiteral import LilyPondLiteral


@functools.total_ordering
class MetronomeMark(AbjadValueObject):
    r"""
    MetronomeMark.

    ..  container:: example

        Initializes integer-valued metronome mark:

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), 90)
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
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

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), abjad.Fraction(181, 2))
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score
                                    \with
                                    {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    }
                                    <<
                                        \new RhythmicStaff
                                        \with
                                        {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.minimum-length = #4
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                            \override TupletNumber.font-size = #0
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        }
                                        {
                                            c'4
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        =
                        \raise
                            #-0.5
                            {
                                90
                                \tiny
                                    \fraction
                                        1
                                        2
                            }
                        }
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    ..  container:: example

        Initializes from text, duration and range:

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> mark = abjad.MetronomeMark((1, 4), (120, 133), 'Quick')
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
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

        Use rational-value units-per-minute together with custom markup for
        float-valued metornome marks:

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
        ...     abjad.Duration(1, 4),
        ...     90.1,
        ...     )
        >>> mark = abjad.MetronomeMark(
        ...     (1, 4),
        ...     Fraction(900, 10),
        ...     custom_markup=markup,
        ...     )
        >>> abjad.attach(mark, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    \tempo \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score
                                    \with
                                    {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    }
                                    <<
                                        \new RhythmicStaff
                                        \with
                                        {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.minimum-length = #4
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                            \override TupletNumber.font-size = #0
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        }
                                        {
                                            c'4
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        =
                        \general-align
                            #Y
                            #-0.5
                            90.1
                        }
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

        (Abjad models all timekeeping with rationals.)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_custom_markup',
        '_hide',
        '_reference_duration',
        '_textual_indication',
        '_units_per_minute',
        )

    _context = 'Score'

    _format_slot = 'opening'

    _parameter = 'METRONOME_MARK'

    ### INITIALIZER ###

    def __init__(
        self,
        reference_duration: typing.Union[
            Duration, typing.Tuple[int, int]] = None,
        units_per_minute: typings.Number = None,
        textual_indication: Markup = None,
        *,
        custom_markup: Markup = None,
        hide: bool = None,
        ) -> None:
        assert isinstance(textual_indication, (str, type(None)))
        arguments = (reference_duration, units_per_minute, textual_indication)
        if all(_ is None for _ in arguments):
            reference_duration = (1, 4)
            units_per_minute = 60
        if reference_duration:
            reference_duration = Duration(reference_duration)
        if isinstance(units_per_minute, float):
            raise Exception(
                f'do not set units-per-minute to float ({units_per_minute});'
                ' use fraction with textual indication instead.'
                )
        prototype = (
            int,
            Fraction,
            collections.Sequence,
            type(None),
            )
        assert isinstance(units_per_minute, prototype)
        if isinstance(units_per_minute, collections.Sequence):
            assert len(units_per_minute) == 2
            item_prototype = (int, Duration)
            assert units_per_minute is not None
            assert all(isinstance(x, item_prototype) for x in units_per_minute)
            units_per_minute = tuple(sorted(units_per_minute))
        self._reference_duration = reference_duration
        self._textual_indication = textual_indication
        self._units_per_minute = units_per_minute
        if custom_markup is not None:
            assert isinstance(custom_markup, Markup), repr(custom_markup)
        self._custom_markup = custom_markup
        if hide is not None:
            hide = bool(hide)
        self._hide = hide

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> typing.Optional['MetronomeMark']:
        """
        Adds metronome mark to ``argument``.

        ..  container:: example

            Adds one metronome mark to another:

            >>> mark_1 = abjad.MetronomeMark((1, 4), 60)
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=150)

            >>> mark_2 + mark_1
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=150)

        ..  container:: example

            Raises imprecise metronome mark error with textual indication:

            >>> mark_1 = abjad.MetronomeMark(textual_indication='Langsam')
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            Traceback (most recent call last):
                ...
            abjad.exceptions.ImpreciseMetronomeMarkError

        ..  container:: example

            Raises imprecise metronome mark error with range:

            >>> mark_1 = abjad.MetronomeMark((1, 8), (90, 92))
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            Traceback (most recent call last):
                ...
            abjad.exceptions.ImpreciseMetronomeMarkError

        ..  container:: example

            Raises type error when ``argument`` is not a metronome mark:

            >>> abjad.MetronomeMark((1, 4), 60) + 90
            Traceback (most recent call last):
                ...
            TypeError: 90

        """
        if not isinstance(argument, type(self)):
            raise TypeError(argument)
        if self.is_imprecise or argument.is_imprecise:
            raise exceptions.ImpreciseMetronomeMarkError
        assert isinstance(self.quarters_per_minute, Fraction)
        assert isinstance(argument.quarters_per_minute, Fraction)
        assert isinstance(self.reference_duration, Duration)
        assert isinstance(argument.reference_duration, Duration)
        new_quarters_per_minute = \
            self.quarters_per_minute + argument.quarters_per_minute
        minimum_denominator = min((
            self.reference_duration.denominator,
            argument.reference_duration.denominator,
            ))
        nonreduced_fraction = NonreducedFraction(new_quarters_per_minute / 4)
        nonreduced_fraction = nonreduced_fraction.with_denominator(
            minimum_denominator)
        new_units_per_minute, new_reference_duration_denominator = \
            nonreduced_fraction.pair
        new_reference_duration = Duration(
            1,
            new_reference_duration_denominator
            )
        metronome_mark = type(self)(
            new_reference_duration,
            new_units_per_minute,
            )
        return metronome_mark

    def __div__(self, argument) -> 'MetronomeMark':
        """
        Divides metronome mark by ``argument``.

        ..  container:: example

            Divides metronome mark by number:

            >>> abjad.MetronomeMark((1, 4), 60) / 2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            Divides metronome mark by other metronome mark:

            >>> abjad.MetronomeMark((1, 4), 60) / abjad.MetronomeMark((1, 4), 40)
            Multiplier(3, 2)

        """
        if self.is_imprecise:
            raise exceptions.ImpreciseMetronomeMarkError
        if getattr(argument, 'is_imprecise', False):
            raise exceptions.ImpreciseMetronomeMarkError
        assert isinstance(self.quarters_per_minute, Fraction)
        if isinstance(argument, type(self)):
            assert isinstance(argument.quarters_per_minute, Fraction)
            result = self.quarters_per_minute / argument.quarters_per_minute
            return Multiplier(result)
        elif isinstance(argument, (int, Fraction)):
            assert isinstance(self.units_per_minute, (int, Fraction))
            units_per_minute = self.units_per_minute / argument
            if mathtools.is_integer_equivalent_number(units_per_minute):
                units_per_minute = int(units_per_minute)
            else:
                units_per_minute = Fraction(units_per_minute)
            result = new(self, units_per_minute=units_per_minute)
            return result
        else:
            raise TypeError(f'must be number or metronome mark: {argument!r}.')

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
        if (self.reference_duration == argument.reference_duration and
            self.units_per_minute == argument.units_per_minute and
            self.textual_indication == argument.textual_indication and
            self.custom_markup == argument.custom_markup):
            return True
        return False

    def __format__(self, format_specification='') -> str:
        r"""
        Formats metronome mark.

        ..  container:: example

            Without custom markup:

            >>> mark = abjad.MetronomeMark((1, 4), 84, 'Allegro')
            >>> print(format(mark))
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=84,
                textual_indication='Allegro',
                )

        ..  container:: example

            With custom markup:

            >>> markup = abjad.Markup(r'\italic { Allegro }')
            >>> mark = abjad.MetronomeMark((1, 4), 84, custom_markup=markup)
            >>> print(format(mark))
            abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=84,
                custom_markup=abjad.Markup(
                    contents=[
                        abjad.MarkupCommand(
                            'italic',
                            ['Allegro']
                            ),
                        ],
                    ),
                )

        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        assert format_specification == 'lilypond'
        return self._get_lilypond_format()

    def __hash__(self) -> int:
        """
        Hashes metronome mark.

        Redefined in tandem with __eq__.
        """
        return AbjadValueObject.__hash__(self)

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a metronome mark with quarters per
        minute greater than that of this metronome mark.
        """
        assert isinstance(argument, type(self)), repr(argument)
        self_quarters_per_minute = self.quarters_per_minute or 0
        argument_quarters_per_minute = argument.quarters_per_minute or 0
        assert isinstance(self_quarters_per_minute, (int, float, Fraction))
        assert isinstance(argument_quarters_per_minute, (int, float, Fraction))
        return self_quarters_per_minute < argument_quarters_per_minute

    def __mul__(self, multiplier) -> typing.Optional['MetronomeMark']:
        """
        Multiplies metronome mark by ``multiplier``.

        ..  container:: example

            Doubles metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 84)
            >>> 2 * mark
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container:: example

            Triples metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 84)
            >>> 3 * mark
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=252)

        """
        if not isinstance(multiplier, (int, float, Duration)):
            return None
        if self.is_imprecise:
            raise exceptions.ImpreciseMetronomeMarkError
        assert isinstance(self.units_per_minute, (int, float, Fraction))
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = Duration(self.reference_duration)
        metronome_mark = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return metronome_mark

    def __radd__(self, argument) -> typing.Optional['MetronomeMark']:
        """
        Adds ``argument`` to metronome mark.

        ..  container:: example

            Adds one metronome mark to another:

            >>> mark_1 = abjad.MetronomeMark((1, 4), 60)
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=150)

            >>> mark_2 + mark_1
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=150)

        ..  container:: example

            Raises imprecise metronome mark error with textual indication:

            >>> mark_1 = abjad.MetronomeMark(textual_indication='Langsam')
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            Traceback (most recent call last):
                ...
            abjad.exceptions.ImpreciseMetronomeMarkError

        ..  container:: example

            Raises imprecise metronome mark error with range:

            >>> mark_1 = abjad.MetronomeMark((1, 8), (90, 92))
            >>> mark_2 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_1 + mark_2
            Traceback (most recent call last):
                ...
            abjad.exceptions.ImpreciseMetronomeMarkError

        ..  container:: example

            Raises type error when ``argument`` is not a metronome mark:

            >>> 90 + abjad.MetronomeMark((1, 4), 60)
            Traceback (most recent call last):
                ...
            TypeError: 90

        """
        if not isinstance(argument, type(self)):
            raise TypeError(argument)
        return argument.__add__(self)

    def __rmul__(self, multiplier) -> typing.Optional['MetronomeMark']:
        """
        Multiplies ``multiplier`` by metronome mark.

        ..  container::: example

            Doubles metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 84)
            >>> mark * 2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=168)

        ..  container::: example

            Triples metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 84)
            >>> mark * 3
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=252)

        """
        if not isinstance(multiplier, (int, float, Duration)):
            return None
        if self.is_imprecise:
            raise exceptions.ImpreciseMetronomeMarkError
        assert isinstance(self.units_per_minute, (int, float, Fraction))
        new_units_per_minute = multiplier * self.units_per_minute
        new_reference_duration = Duration(self.reference_duration)
        metronome_mark = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return metronome_mark

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

            >>> mark = abjad.MetronomeMark((1, 4), (90, 96))
            >>> str(mark)
            '4=90-96'

        """
        if self.textual_indication is not None:
            string = self.textual_indication
        elif isinstance(self.units_per_minute, (int, float)):
            string = f'{self._dotted}={self.units_per_minute}'
        elif (isinstance(self.units_per_minute, Fraction) and
            not mathtools.is_integer_equivalent_number(self.units_per_minute)):
            integer_part = int(float(self.units_per_minute))
            remainder = self.units_per_minute - integer_part
            remainder = Fraction(remainder)
            string = f'{self._dotted}={integer_part}+{remainder}'
        elif (isinstance(self.units_per_minute, Fraction) and
            mathtools.is_integer_equivalent_number(self.units_per_minute)):
            string = '{}={}'
            integer = int(float(self.units_per_minute))
            string = string.format(self._dotted, integer)
        elif isinstance(self.units_per_minute, tuple):
            string = '{}={}-{}'
            string = string.format(
                self._dotted,
                self.units_per_minute[0],
                self.units_per_minute[1],
                )
        else:
            raise TypeError(f'unknown: {self.units_per_minute!r}.')
        return string

    def __sub__(self, argument) -> 'MetronomeMark':
        """
        Subtracts ``argument`` from metronome mark.

        ..  container:: example

            Same reference reference durations:

            >>> mark_1 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_2 = abjad.MetronomeMark((1, 4), 60)
            >>> mark_1 - mark_2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            Different reference durations:

            >>> mark_1 = abjad.MetronomeMark((1, 4), 90)
            >>> mark_2 = abjad.MetronomeMark((1, 2), 90)
            >>> mark_1 - mark_2
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=45)

        ..  container:: example

            Raises imprecise metronome mark error with textual indication:

            >>> mark_1 = abjad.MetronomeMark(textual_indication='Langsam')
            >>> mark_2 = abjad.MetronomeMark((1, 2), 90)
            >>> mark_1 - mark_2
            Traceback (most recent call last):
                ...
            abjad.exceptions.ImpreciseMetronomeMarkError

        """
        if not isinstance(argument, type(self)):
            raise Exception('must be metronome mark: {argument!r}.')
        if self.is_imprecise or argument.is_imprecise:
            raise exceptions.ImpreciseMetronomeMarkError
        assert isinstance(self.quarters_per_minute, (int, float, Fraction))
        assert isinstance(argument.quarters_per_minute, (int, float, Fraction))
        assert isinstance(self.reference_duration, Duration)
        assert isinstance(argument.reference_duration, Duration)
        new_quarters_per_minute = self.quarters_per_minute - \
            argument.quarters_per_minute
        minimum_denominator = min((
            self.reference_duration.denominator,
            argument.reference_duration.denominator,
            ))
        nonreduced_fraction = NonreducedFraction(new_quarters_per_minute / 4)
        nonreduced_fraction = nonreduced_fraction.with_denominator(
            minimum_denominator)
        new_units_per_minute, new_reference_duration_denominator = \
            nonreduced_fraction.pair
        new_reference_duration = Duration(
            1,
            new_reference_duration_denominator,
            )
        metronome_mark = type(self)(
            reference_duration=new_reference_duration,
            units_per_minute=new_units_per_minute,
            )
        return metronome_mark

    def __truediv__(self, argument) -> 'MetronomeMark':
        """
        Divides metronome mark by ``argument``.

        Operator required by Python 3.

        ..  container:: example

            Divides metronome mark by number:

            >>> abjad.MetronomeMark((1, 4), 60).__truediv__(2)
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=30)

        ..  container:: example

            Divides metronome mark by other metronome mark:

            >>> abjad.MetronomeMark((1, 4), 60).__truediv__(
            ...     abjad.MetronomeMark((1, 4), 40)
            ...     )
            Multiplier(3, 2)

        """
        return self.__div__(argument)

    ### PRIVATE PROPERTIES ###

    @property
    def _dotted(self):
        return self.reference_duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.reference_duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            string = '{}={}-{}'
            string = string.format(
                self._dotted,
                self.units_per_minute[0],
                self.units_per_minute[1],
                )
            return string
        elif isinstance(self.units_per_minute, (float, Fraction)):
            markup = MetronomeMark.make_tempo_equation_markup(
                self.reference_duration,
                self.units_per_minute,
                )
            string = str(markup)
            return string
        string = f'{self._dotted}={self.units_per_minute}'
        return string

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = self.textual_indication
            text = Scheme.format_scheme_value(text)
        if (self.reference_duration is not None and
            self.units_per_minute is not None):
            equation = self._equation
        if self.custom_markup is not None:
            return rf'\tempo {self.custom_markup}'
        elif text and equation:
            return rf'\tempo {text} {equation}'
        elif equation:
            return rf'\tempo {equation}'
        elif text:
            return rf'\tempo {text}'
        else:
            return r'\tempo \default'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.hide:
            bundle.before.commands.append(self._get_lilypond_format())
        return bundle

    def _make_lhs_score_markup(self, reference_duration=None):
        import abjad
        reference_duration = reference_duration or self.reference_duration
        maker = abjad.NoteMaker()
        selection = maker([0], [reference_duration])
        markup = Duration._to_score_markup(selection)
        return markup

    def _get_markup(self, stem_height=1):
        if self.custom_markup is not None:
            return self.custom_markup
        duration_log = int(math.log(self.reference_duration.denominator, 2))
        markup = Markup.abjad_metronome_mark(
            duration_log,
            self.reference_duration.dot_count,
            stem_height,
            self.units_per_minute,
            )
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def custom_markup(self) -> typing.Optional[Markup]:
        r"""
        Gets custom markup of metronome mark.

        ..  container:: example

            With custom markup:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     abjad.Duration(1, 4),
            ...     67.5,
            ...     )
            >>> markup = markup.with_color('red')
            >>> mark = abjad.MetronomeMark(
            ...     reference_duration=(1, 4),
            ...     units_per_minute=Fraction(135, 2),
            ...     custom_markup=markup,
            ...     )
            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        \tempo \markup {
                            \with-color
                                #red
                                {
                                    \scale
                                        #'(0.75 . 0.75)
                                        \score
                                            {
                                                \new Score
                                                \with
                                                {
                                                    \override SpacingSpanner.spacing-increment = #0.5
                                                    proportionalNotationDuration = ##f
                                                }
                                                <<
                                                    \new RhythmicStaff
                                                    \with
                                                    {
                                                        \remove Time_signature_engraver
                                                        \remove Staff_symbol_engraver
                                                        \override Stem.direction = #up
                                                        \override Stem.length = #5
                                                        \override TupletBracket.bracket-visibility = ##t
                                                        \override TupletBracket.direction = #up
                                                        \override TupletBracket.minimum-length = #4
                                                        \override TupletBracket.padding = #1.25
                                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                        \override TupletNumber.font-size = #0
                                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                        tupletFullLength = ##t
                                                    }
                                                    {
                                                        c'4
                                                    }
                                                >>
                                                \layout {
                                                    indent = #0
                                                    ragged-right = ##t
                                                }
                                            }
                                    =
                                    \general-align
                                        #Y
                                        #-0.5
                                        67.5
                                }
                            }
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>

        """
        return self._custom_markup

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            Fifty-two eighth notes per minute:

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.context
            'Score'

        ..  container:: example

            Ninety quarter notes per minute:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> mark.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when metronome mark should not appear in output (but
        should still determine effective metronome mark).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> metronome_mark_1 = abjad.MetronomeMark((1, 4), 72)
            >>> abjad.attach(metronome_mark_1, staff[0]) 
            >>> metronome_mark_2 = abjad.MetronomeMark(
            ...     textual_indication='Allegro',
            ...     hide=True,
            ...     )
            >>> abjad.attach(metronome_mark_2, staff[2]) 
            >>> score = abjad.Score([staff])
            >>> abjad.show(score) # doctest: +SKIP

            >>> abjad.f(score)
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

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     prototype = abjad.MetronomeMark
            ...     leaf, abjad.inspect(leaf).effective(prototype)
            ...
            (Note("c'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72))
            (Note("d'4"), MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=72))
            (Note("e'4"), MetronomeMark(textual_indication='Allegro', hide=True))
            (Note("f'4"), MetronomeMark(textual_indication='Allegro', hide=True))

        """
        return self._hide

    @property
    def is_imprecise(self) -> bool:
        """
        Is true if metronome mark is entirely textual or if metronome
        mark's units_per_minute is a range.

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
    def parameter(self) -> str:
        """
        Is ``'METRONOME_MARK'``.

        ..  container:: example

            >>> abjad.MetronomeMark((1, 8), 52).parameter
            'METRONOME_MARK'

        """
        return self._parameter

    @property
    def quarters_per_minute(self) -> typing.Union[tuple, None, Fraction]:
        """
        Gets metronome mark quarters per minute.

        ..  container:: example

            Fifty-two eighth notes per minute:

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.quarters_per_minute
            Fraction(104, 1)

        ..  container:: example

            Ninety quarter notes per minute:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> mark.quarters_per_minute
            Fraction(90, 1)

        ..  container:: example

            140 quarters per minute:

            >>> mark = abjad.MetronomeMark((3, 32), Fraction(105, 2))
            >>> mark.quarters_per_minute
            Fraction(140, 1)

        Returns tuple when metronome mark ``units_per_minute`` is a range.

        Returns none when metronome mark is imprecise.

        Returns fraction otherwise.
        """
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[0]
            high = Duration(1, 4) / self.reference_duration * \
                self.units_per_minute[1]
            return (low, high)
        result = Duration(1, 4) / self.reference_duration * \
            self.units_per_minute
        return Fraction(result)

    @property
    def reference_duration(self) -> typing.Optional[Duration]:
        """
        Gets reference duration of metronome mark.

        ..  container:: example

            Fifty-two eighth notes per minute:

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.reference_duration
            Duration(1, 8)

        ..  container:: example

            Ninety quarter notes per minute:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> mark.reference_duration
            Duration(1, 4)

        """
        return self._reference_duration

    @property
    def textual_indication(self) -> typing.Optional[str]:
        """
        Gets optional textual indication of metronome mark.

        ..  container:: example

            Fifty-two eighth notes per minute:

            >>> mark = abjad.MetronomeMark((1, 8), 52)
            >>> mark.textual_indication is None
            True

        ..  container:: example

            Ninety quarter notes per minute:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> mark.textual_indication is None
            True

        """
        return self._textual_indication

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on metronome mark.
        
        The LilyPond ``\tempo`` command refuses tweaks.

        Override the LilyPond ``MetronomeMark`` grob instead.
        """
        pass

    @property
    def units_per_minute(self) -> typing.Union[int, Fraction, None]:
        """
        Gets units per minute of metronome mark.

        ..  container:: example

            Integer-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), 90)
            >>> mark.units_per_minute
            90

        ..  container:: example

            Rational-valued metronome mark:

            >>> mark = abjad.MetronomeMark((1, 4), abjad.Fraction(181, 2))
            >>> mark.units_per_minute
            Fraction(181, 2)

        """
        return self._units_per_minute

    ### PUBLIC METHODS ###

    def duration_to_milliseconds(self, duration) -> Duration:
        """
        Gets millisecond value of ``duration`` under a given metronome mark.

        ..  container:: example

            One quarter lasts 1000 msec at quarter equals 60:

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> mark.duration_to_milliseconds((1, 4))
            Duration(1000, 1)

        ..  container:: example

            Dotted sixteenth lasts 1500 msec at quarter equals 60:

            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> mark.duration_to_milliseconds((3, 8))
            Duration(1500, 1)

        """
        assert isinstance(self.reference_duration, Duration)
        denominator = self.reference_duration.denominator
        numerator = self.reference_duration.numerator
        whole_note_duration = 1000
        whole_note_duration *= Multiplier(denominator, numerator)
        whole_note_duration *= Multiplier(60, self.units_per_minute)
        duration = Duration(duration)
        return Duration(duration * whole_note_duration)

    def list_related_tempos(
        self,
        maximum_numerator=None,
        maximum_denominator=None,
        integer_tempos_only=False,
        ):
        r"""
        Lists related tempos.

        ..  container:: example

            Rewrites tempo ``4=58`` by ratios ``n:d`` such that ``1 <= n <= 8``
            and ``1 <= d <= 8``.

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=8,
            ...     maximum_denominator=8,
            ...     )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}\t{ratio!s}'
            ...     print(string)
            4=29        1:2
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
            4=58        1:1
            4=66+2/7    8:7
            4=67+2/3    7:6
            4=69+3/5    6:5
            4=72+1/2    5:4
            4=77+1/3    4:3
            4=81+1/5    7:5
            4=87        3:2
            4=92+4/5    8:5
            4=96+2/3    5:3
            4=101+1/2   7:4
            4=116       2:1

        ..  container:: example

            Integer-valued tempos only:

            >>> mark = abjad.MetronomeMark((1, 4), 58)
            >>> pairs = mark.list_related_tempos(
            ...     maximum_numerator=16,
            ...     maximum_denominator=16,
            ...     integer_tempos_only=True,
            ...     )

            >>> for tempo, ratio in pairs:
            ...     string = f'{tempo!s}\t{ratio!s}'
            ...     print(string)
            4=29	1:2
            4=58	1:1
            4=87	3:2
            4=116	2:1

        Constrains ratios such that ``1:2 <= n:d <= 2:1``.

        Returns list of tempo / ratio pairs.
        """
        allowable_numerators = range(1, maximum_numerator + 1)
        allowable_denominators = range(1, maximum_denominator + 1)
        numbers = [allowable_numerators, allowable_denominators]
        enumerator = Enumerator(numbers)
        pairs = enumerator.yield_outer_product()
        multipliers = [Multiplier(_) for _ in pairs]
        multipliers = [
            _ for _ in multipliers
            if Fraction(1, 2) <= _ <= Fraction(2)
            ]
        multipliers.sort()
        multipliers = sequence(multipliers).remove_repeats()
        pairs = []
        for multiplier in multipliers:
            new_units_per_minute = multiplier * self.units_per_minute
            if (integer_tempos_only and not
                mathtools.is_integer_equivalent_number(new_units_per_minute)):
                continue
            metronome_mark = type(self)(
                reference_duration=self.reference_duration,
                units_per_minute=new_units_per_minute,
                )
            ratio = Ratio(multiplier.pair)
            pair = (metronome_mark, ratio)
            pairs.append(pair)
        return pairs

    @staticmethod
    def make_tempo_equation_markup(reference_duration, units_per_minute):
        r"""
        Makes tempo equation markup.

        ..  container:: example

            Integer-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     (1, 4),
            ...     90,
            ...     )
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            Float-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     (1, 4),
            ...     90.1,
            ...     )
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90.1
                    }

        ..  container:: example

            Rational-valued metronome mark:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     abjad.Duration(1, 4),
            ...     abjad.Fraction(181, 2),
            ...     )
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \raise
                        #-0.5
                        {
                            90
                            \tiny
                                \fraction
                                    1
                                    2
                        }
                    }

        ..  container:: example

            Reference duration expressed with ties:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(
            ...     (5, 16),
            ...     90,
            ...     )
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4
                                        ~
                                        c'16
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            Reference duration expressed as a tuplet:

            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup((1, 6), 90)
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        \tweak edge-height #'(0.7 . 0)
                                        \times 2/3 {
                                            c'4
                                        }
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

        ..  container:: example

            Reference duration passed in as explicit rhythm:

            >>> maker = abjad.NoteMaker()
            >>> durations = [(1, 16), (3, 16), (1, 16)]
            >>> selection = maker([0], durations)
            >>> abjad.attach(abjad.Tie(), selection)
            >>> abjad.attach(abjad.Beam(), selection)
            >>> markup = abjad.MetronomeMark.make_tempo_equation_markup(selection, 90)
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> print(format(markup))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'16
                                        ~
                                        [
                                        c'8.
                                        ~
                                        c'16
                                        ]
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \general-align
                        #Y
                        #-0.5
                        90
                    }

            Pass rhythms like this as Abjad selections.

        Returns markup.
        """
        import abjad
        if isinstance(reference_duration, abjad.Selection):
            selection = reference_duration
        else:
            maker = abjad.NoteMaker()
            selection = maker([0], [reference_duration])
        lhs_score_markup = Duration._to_score_markup(selection)
        lhs_score_markup = lhs_score_markup.scale((0.75, 0.75))
        equal_markup = abjad.Markup('=')
        if (isinstance(units_per_minute, abjad.Fraction) and
            not abjad.mathtools.is_integer_equivalent_number(units_per_minute)):
            rhs_markup = abjad.Markup.make_improper_fraction_markup(
                units_per_minute)
            rhs_markup = rhs_markup.raise_(-0.5)
        else:
            rhs_markup = abjad.Markup(units_per_minute)
            rhs_markup = rhs_markup.general_align('Y', -0.5)
        markup = lhs_score_markup + equal_markup + rhs_markup
        return markup

    def rewrite_duration(self, duration, metronome_mark):
        r"""
        Rewrites ``duration`` under ``metronome_mark``.

        ..  container:: example

            Consider the two metronome marks below.

            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> metronome_mark = abjad.MetronomeMark((1, 4), 90)

            ``tempo`` specifies quarter equal to ``60``.

            ``metronome_mark`` indication specifies quarter equal to ``90``.

            ``metronome_mark`` is ``3/2`` times as fast as ``tempo``:

            >>> metronome_mark / tempo
            Multiplier(3, 2)

            Note that a triplet eighth note under ``tempo`` equals a regular
            eighth note under ``metronome_mark``:

            >>> tempo.rewrite_duration((1, 12), metronome_mark)
            Duration(1, 8)

            And note that a regular eighth note under ``tempo`` equals a dotted
            sixteenth under ``metronome_mark``:

            >>> tempo.rewrite_duration((1, 8), metronome_mark)
            Duration(3, 16)

        Given ``duration`` governed by this tempo returns new duration governed
        by ``metronome_mark``.

        Ensures that ``duration`` and new duration consume the same amount of
        time in seconds.

        Returns duration.
        """
        import abjad
        duration = Duration(duration)
        tempo_ratio = metronome_mark / self
        new_duration = tempo_ratio * duration
        return new_duration
