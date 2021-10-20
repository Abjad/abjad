import dataclasses
import typing

from .. import duration as _duration
from .. import math as _math


@dataclasses.dataclass(order=True, unsafe_hash=True)
class TimeSignature:
    r"""
    Time signature.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

    ..  container:: example

        Create score-contexted time signatures like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0], context="Score")

        Score-contexted time signatures format behind comments when no Abjad score
        container is found:

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            %%% \time 3/8 %%%
            c'8
            d'8
            e'8
            c'8
            d'8
            e'8
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Score-contexted time signatures format normally when an Abjad score container is
        found:

        >>> score = abjad.Score([staff])
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                \time 3/8
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

        >>> abjad.show(score) # doctest: +SKIP

    ..  container:: example

        Time signatures can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(
        ...     time_signature,
        ...     staff[0],
        ...     context="Score",
        ...     tag=abjad.Tag("+PARTS"),
        ... )
        >>> score = abjad.Score([staff])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(score, tags=True)
        >>> print(string)
        \new Score
        <<
            \new Staff
            {
                %! +PARTS
                \time 3/8
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

    ..  container:: example

        Set ``hide=True`` time signature should not appear in output (but should still
        determine effective time signature):

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> time_signature = abjad.TimeSignature((4, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> time_signature = abjad.TimeSignature((2, 4), hide=True)
        >>> abjad.attach(time_signature, staff[2])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

        >>> for leaf in abjad.iterate.leaves(staff):
        ...     prototype = abjad.TimeSignature
        ...     leaf, abjad.get.effective(leaf, prototype)
        ...
        (Note("c'4"), TimeSignature(pair=(4, 4), hide=False, partial=None))
        (Note("d'4"), TimeSignature(pair=(4, 4), hide=False, partial=None))
        (Note("e'4"), TimeSignature(pair=(2, 4), hide=True, partial=None))
        (Note("f'4"), TimeSignature(pair=(2, 4), hide=True, partial=None))

    """

    pair: tuple[int, int]
    hide: bool = False
    partial: typing.Optional[_duration.Duration] = None

    _is_dataclass = True

    _format_slot = "opening"

    # TODO: context should probably be "Score"
    context = "Staff"
    persistent = True

    def __post_init__(self):
        pair_ = getattr(self.pair, "pair", self.pair)
        assert len(pair_) == 2, repr(pair_)
        assert isinstance(pair_[0], int)
        assert isinstance(pair_[1], int)
        numerator, denominator = pair_
        self.pair = (numerator, denominator)
        if self.partial is not None:
            self.partial = _duration.Duration(self.partial)

    def __copy__(self, *arguments) -> "TimeSignature":
        """
        Copies time signature.
        """
        return type(self)((self.numerator, self.denominator), partial=self.partial)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a time signature with numerator and denominator
        equal to this time signature. Also true when ``argument`` is a tuple with first
        and second elements equal to numerator and denominator of this time signature.
        """
        if isinstance(argument, type(self)):
            if self.numerator == argument.numerator:
                if self.denominator == argument.denominator:
                    return True
        return False

    def __str__(self) -> str:
        """
        Gets string representation of time signature.

        ..  container:: example

            >>> str(abjad.TimeSignature((3, 8)))
            '3/8'

        """
        return f"{self.numerator}/{self.denominator}"

    def _get_lilypond_format(self):
        result = []
        if self.hide:
            return result
        if self.is_non_dyadic_rational:
            string = '#(ly:expect-warning "strange time signature found")'
            result.append(string)
        if self.partial is None:
            result.append(rf"\time {self.numerator}/{self.denominator}")
        else:
            duration_string = self.partial.lilypond_duration_string
            partial_directive = rf"\partial {duration_string}"
            result.append(partial_directive)
            string = rf"\time {self.numerator}/{self.denominator}"
            result.append(string)
        return result

    @property
    def denominator(self) -> int:
        """
        Gets denominator of time signature:

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).denominator
            8

        """
        return self.pair[1]

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).duration
            Duration(3, 8)

        """
        return _duration.Duration(*self.pair)

    @property
    def is_non_dyadic_rational(self) -> bool:
        r"""
        Is true when time signature has non-power-of-two denominator.

        ..  container:: example

            With non-power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((7, 12))
            >>> time_signature.is_non_dyadic_rational
            True

            With power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> time_signature.is_non_dyadic_rational
            False

            Suppresses LilyPond "strange time signature" warning:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d' e' f'")
            >>> staff = abjad.Staff([tuplet])
            >>> time_signature = abjad.TimeSignature((4, 3))
            >>> abjad.attach(time_signature, tuplet[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    #(ly:expect-warning "strange time signature found")
                    \time 4/3
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }

        """
        return not _math.is_nonnegative_integer_power_of_two(self.denominator)

    @property
    def implied_prolation(self) -> _duration.Multiplier:
        """
        Gets implied prolation of time signature.

        ..  container:: example

            Implied prolation of dyadic time signature:

            >>> abjad.TimeSignature((3, 8)).implied_prolation
            Multiplier(1, 1)

            Implied prolation of nondyadic time signature:

            >>> abjad.TimeSignature((7, 12)).implied_prolation
            Multiplier(2, 3)

        """
        return _duration.Duration(1, self.denominator).implied_prolation

    @property
    def numerator(self) -> int:
        """
        Gets numerator of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).numerator
            3

        """
        return self.pair[0]

    @staticmethod
    def from_string(string) -> "TimeSignature":
        """
        Makes new time signature from fraction ``string``.

        ..  container:: example

            >>> abjad.TimeSignature.from_string("6/8")
            TimeSignature(pair=(6, 8), hide=False, partial=None)

        """
        assert isinstance(string, str), repr(string)
        parts = string.split("/")
        assert len(parts) == 2, repr(parts)
        numbers = [int(_) for _ in parts]
        numerator, denominator = numbers
        return TimeSignature((numerator, denominator))

    # TODO: remove contents_multiplier?
    # TODO: rename to to_dyadic_rational()
    def is_dyadic_rational(self, contents_multiplier=1) -> "TimeSignature":
        """
        Makes new time signature equivalent to current time signature with power-of-two
        denominator.

        ..  container:: example

            >>> abjad.TimeSignature((1, 12)).is_dyadic_rational()
            TimeSignature(pair=(1, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 12)).is_dyadic_rational()
            TimeSignature(pair=(2, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 12)).is_dyadic_rational()
            TimeSignature(pair=(2, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 12)).is_dyadic_rational()
            TimeSignature(pair=(4, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 12)).is_dyadic_rational()
            TimeSignature(pair=(5, 12), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 12)).is_dyadic_rational()
            TimeSignature(pair=(4, 8), hide=False, partial=None)

            >>> abjad.TimeSignature((1, 14)).is_dyadic_rational()
            TimeSignature(pair=(1, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((2, 14)).is_dyadic_rational()
            TimeSignature(pair=(2, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((3, 14)).is_dyadic_rational()
            TimeSignature(pair=(3, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((4, 14)).is_dyadic_rational()
            TimeSignature(pair=(4, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((5, 14)).is_dyadic_rational()
            TimeSignature(pair=(5, 14), hide=False, partial=None)

            >>> abjad.TimeSignature((6, 14)).is_dyadic_rational()
            TimeSignature(pair=(6, 14), hide=False, partial=None)

        """
        contents_multiplier = _duration.Multiplier(contents_multiplier)
        contents_multiplier = _duration.Multiplier(contents_multiplier)
        non_power_of_two_denominator = self.denominator
        if contents_multiplier == _duration.Multiplier(1):
            power_of_two_denominator = _math.greatest_power_of_two_less_equal(
                non_power_of_two_denominator
            )
        else:
            power_of_two_denominator = _math.greatest_power_of_two_less_equal(
                non_power_of_two_denominator, 1
            )
        non_dyadic_rational_pair = _duration.NonreducedFraction(self.pair)
        dyadic_rational = non_dyadic_rational_pair.with_denominator(
            power_of_two_denominator
        )
        dyadic_rational_pair = dyadic_rational.pair
        return type(self)(dyadic_rational_pair)
