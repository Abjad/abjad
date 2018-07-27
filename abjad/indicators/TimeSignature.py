import collections
import typing
from abjad import mathtools
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.Duration import Duration
from abjad.utilities.Multiplier import Multiplier


class TimeSignature(AbjadValueObject):
    r"""
    Time signature.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8")
        >>> time_signature = abjad.TimeSignature((3, 8))
        >>> abjad.attach(time_signature, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
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
        >>> abjad.attach(time_signature, staff[0], context='Score')

        Score-contexted time signatures format behind comments when no Abjad
        score container is found:

        >>> abjad.f(staff)
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

        Score-contexted time signatures format normally when an Abjad score
        container is found:

        >>> score = abjad.Score([staff])
        >>> abjad.f(score)
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
        >>> abjad.attach(time_signature, staff[0], context='Score', tag='RED')
        >>> score = abjad.Score([staff])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 3/8 %! RED
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_denominator',
        '_has_non_power_of_two_denominator',
        '_hide',
        '_multiplier',
        '_numerator',
        '_partial',
        '_partial_repr_string',
        )

    _context = 'Staff'

    _format_slot = 'opening'

    _parameter = True

    ### INITIALIZER ###

    def __init__(
        self,
        pair: typing.Tuple[int, int] = (4, 4),
        *,
        partial: Duration = None,
        hide: bool = None,
        ) -> None:
        import abjad
        pair = getattr(pair, 'pair', pair)
        assert isinstance(pair, collections.Iterable), repr(pair)
        assert len(pair) == 2, repr(pair)
        numerator, denominator = pair
        assert isinstance(numerator, int), repr(numerator)
        assert isinstance(denominator, int), repr(denominator)
        self._numerator: int = numerator
        self._denominator: int = denominator
        if partial is not None:
            partial = Duration(partial)
        self._partial: typing.Optional[Duration] = partial
        if partial is not None:
            self._partial_repr_string = ', partial=%r' % self._partial
        else:
            self._partial_repr_string = ''
        if hide is not None:
            hide = bool(hide)
        self._hide: typing.Optional[bool] = hide
        self._multiplier = self.implied_prolation
        result = mathtools.is_nonnegative_integer_power_of_two(self.denominator)
        assert isinstance(result, bool)
        self._has_non_power_of_two_denominator: bool = not(result)

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> 'TimeSignature':
        """
        Adds time signature to ``argument``.

        ..  container:: example

            Adds two time signatures with the same denominator:

            >>> abjad.TimeSignature((3, 4)) + abjad.TimeSignature((3, 4))
            TimeSignature((6, 4))

        ..  container:: example

            Adds two time signatures with different denominators:

            >>> abjad.TimeSignature((3, 4)) + abjad.TimeSignature((6, 8))
            TimeSignature((12, 8))

            Returns new time signature in terms of greatest denominator.

        """
        if not isinstance(argument, type(self)):
            raise Exception('must be time signature: {argument!r}.')
        nonreduced_1 = NonreducedFraction(
            self.numerator,
            self.denominator,
            )
        nonreduced_2 = NonreducedFraction(
            argument.numerator,
            argument.denominator,
            )
        result = nonreduced_1 + nonreduced_2
        result = type(self)((
            result.numerator,
            result.denominator,
            ))
        return result

    def __copy__(self, *arguments) -> 'TimeSignature':
        """Copies time signature.
        """
        return type(self)(
            (self.numerator, self.denominator),
            partial=self.partial,
            )

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a time signature with numerator and
        denominator equal to this time signature. Also true when ``argument``
        is a tuple with first and second elements equal to numerator and
        denominator of this time signature.
        """
        # custom definition retained only bc tests currently break with super()
        if isinstance(argument, type(self)):
            return (self.numerator == argument.numerator and
                self.denominator == argument.denominator)
        elif isinstance(argument, tuple):
            return self.numerator == argument[0] and self.denominator == argument[1]
        else:
            return False

    def __format__(self, format_specification='') -> str:
        """
        Formats time signature.

        ..  container:: example

            >>> print(format(abjad.TimeSignature((3, 8))))
            abjad.TimeSignature((3, 8))

        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        assert format_specification == 'lilypond'
        return self._get_lilypond_format()

    def __ge__(self, argument) -> bool:
        """
        Is true when duration of time signature is greater than or equal to
        duration of ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.duration >= argument.duration
        else:
            raise TypeError(argument)

    def __gt__(self, argument) -> bool:
        """
        Is true when duration of time signature is greater than duration of
        ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.duration > argument.duration
        else:
            raise TypeError(argument)

    def __hash__(self) -> int:
        """Hashes time signature.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __le__(self, argument) -> bool:
        """
        Is true when duration of time signature is less than duration of
        ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.duration <= argument.duration
        else:
            raise TypeError(argument)

    def __lt__(self, argument) -> bool:
        """
        Is true when duration of time signature is less than duration of
        ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.duration < argument.duration
        else:
            raise TypeError(argument)

    def __radd__(self, argument) -> 'TimeSignature':
        """
        Adds ``argument`` to time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)) + abjad.TimeSignature((4, 4))
            TimeSignature((11, 8))

        """
        return self.__add__(argument)

    def __str__(self) -> str:
        """
        Gets string representation of time signature.

        ..  container:: example

            >>> str(abjad.TimeSignature((3, 8)))
            '3/8'

        """
        return f'{self.numerator}/{self.denominator}'

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        storage_format_is_indented = False
        if self.partial is not None or self.hide is not None:
            storage_format_is_indented = True
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.pair],
            storage_format_kwargs_names=['partial', 'hide'],
            storage_format_is_indented=storage_format_is_indented,
            )

    def _get_lilypond_format(self):
        if self.hide:
            return []
        elif self.partial is None:
            return rf'\time {self.numerator}/{self.denominator}'
        else:
            result = []
            duration_string = self.partial.lilypond_duration_string
            partial_directive = rf'\partial {duration_string}'
            result.append(partial_directive)
            string = rf'\time {self.numerator}/{self.denominator}'
            result.append(string)
            return result

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets (historically conventional) context.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).context
            'Staff'

        ..  todo:: Should return ``'Score'``.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def denominator(self) -> int:
        """
        Gets denominator of time signature:

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).denominator
            8

        """
        return self._denominator

    @property
    def duration(self) -> Duration:
        """
        Gets duration of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).duration
            Duration(3, 8)

        """
        return Duration(self.numerator, self.denominator)

    @property
    def has_non_power_of_two_denominator(self) -> bool:
        """
        Is true when time signature has non-power-of-two denominator.

        ..  container:: example

            With non-power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((7, 12))
            >>> time_signature.has_non_power_of_two_denominator
            True

        ..  container:: example

            With power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> time_signature.has_non_power_of_two_denominator
            False

        """
        return self._has_non_power_of_two_denominator

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when time signature should not appear in output (but should
        still determine effective time signature).

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> time_signature = abjad.TimeSignature((4, 4))
            >>> abjad.attach(time_signature, staff[0]) 
            >>> time_signature = abjad.TimeSignature((2, 4), hide=True)
            >>> abjad.attach(time_signature, staff[2]) 
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
            }

            >>> for leaf in abjad.iterate(staff).leaves():
            ...     prototype = abjad.TimeSignature 
            ...     leaf, abjad.inspect(leaf).effective(prototype)
            ...
            (Note("c'4"), TimeSignature((4, 4)))
            (Note("d'4"), TimeSignature((4, 4)))
            (Note("e'4"), TimeSignature((2, 4), hide=True))
            (Note("f'4"), TimeSignature((2, 4), hide=True))

        """
        return self._hide

    @property
    def implied_prolation(self) -> Multiplier:
        """
        Gets implied prolation of time signature.

        ..  container:: example

            Implied prolation of time signature with power-of-two denominator:

            >>> abjad.TimeSignature((3, 8)).implied_prolation
            Multiplier(1, 1)

        ..  container:: example

            Implied prolation of time signature with non-power-of-two
            denominator:

            >>> abjad.TimeSignature((7, 12)).implied_prolation
            Multiplier(2, 3)

        """
        dummy_duration = Duration(1, self.denominator)
        return dummy_duration.implied_prolation

    @property
    def numerator(self) -> int:
        """
        Gets numerator of time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).numerator
            3

        """
        return self._numerator

    @property
    def pair(self) -> typing.Tuple[int, int]:
        """
        Gets numerator / denominator pair corresponding to time siganture.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).pair
            (3, 8)

        """
        return (self.numerator, self.denominator)

    @property
    def partial(self) -> typing.Optional[Duration]:
        """
        Gets duration of pick-up to time signature.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).partial is None
            True

        """
        return self._partial

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.TimeSignature((3, 8)).parameter
            True

        """
        return self._parameter

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on time signature.
        
        The LilyPond ``\time`` command refuses tweaks.

        Override the LilyPond ``TimeSignature`` grob instead.
        """
        pass

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string) -> 'TimeSignature':
        """
        Makes new time signature from fraction ``string``.

        ..  container:: example

            >>> abjad.TimeSignature.from_string('6/8')
            TimeSignature((6, 8))

        """
        assert isinstance(string, str), repr(string)
        parts = string.split('/')
        assert len(parts) == 2, repr(parts)
        numbers = [int(_) for _ in parts]
        numerator, denominator = numbers
        return TimeSignature((numerator, denominator))

    def with_power_of_two_denominator(
        self,
        contents_multiplier=1,
        ) -> 'TimeSignature':
        """
        Makes new time signature equivalent to current time signature with
        power-of-two denominator.

        ..  container:: example

            Non-power-of-two denominator with power-of-two denominator:

            >>> time_signature = abjad.TimeSignature((3, 12))
            >>> time_signature.with_power_of_two_denominator()
            TimeSignature((2, 8))

        """
        contents_multiplier = Multiplier(contents_multiplier)
        contents_multiplier = Multiplier(contents_multiplier)
        non_power_of_two_denominator = self.denominator
        if contents_multiplier == Multiplier(1):
            power_of_two_denominator = \
                mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator)
        else:
            power_of_two_denominator = \
                mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator, 1)
        non_power_of_two_pair = NonreducedFraction(self.pair)
        power_of_two_fraction = non_power_of_two_pair.with_denominator(
            power_of_two_denominator)
        power_of_two_pair = power_of_two_fraction.pair
        return type(self)(power_of_two_pair)
