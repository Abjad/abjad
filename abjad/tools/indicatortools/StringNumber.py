import collections
import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StringNumber(AbjadValueObject):
    '''
    String number.

    ..  container:: example

        String I:

        >>> indicator = abjad.StringNumber(1)
        >>> abjad.f(indicator)
        abjad.StringNumber(
            numbers=(1,),
            )

    ..  container:: example

        Strings II and III:

        >>> indicator = abjad.StringNumber((2, 3))
        >>> abjad.f(indicator)
        abjad.StringNumber(
            numbers=(2, 3),
            )

    '''

    ### CLASS VARIABLES

    __slots__ = (
        '_numbers',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        numbers: typing.Union[int, typing.Iterable[int]] = None,
        ) -> None:
        if numbers is None:
            numbers_: typing.Tuple[int, ...] = ()
        elif isinstance(numbers, int):
            numbers_ = (numbers,)
        else:
            numbers_ = tuple(numbers)
        assert isinstance(numbers_, tuple), repr(numbers_)
        numbers_ = tuple(int(_) for _ in numbers_)
        assert all(0 < _ < 7 for _ in numbers_)
        self._numbers = numbers_

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self) -> typing.Tuple[int, ...]:
        '''
        Gets numbers.

        ..  container:: example

            String I:

            >>> indicator = abjad.StringNumber(1)
            >>> indicator.numbers
            (1,)

            >>> indicator = abjad.StringNumber((2, 3))
            >>> indicator.numbers
            (2, 3)

        '''
        return self._numbers

    @property
    def roman_numerals(self) -> typing.Tuple[str, ...]:
        '''
        Gets roman numerals of string number indicator.

        ..  container:: example

            String I:

            >>> indicator = abjad.StringNumber(1)
            >>> indicator.roman_numerals
            ('i',)

        ..  container:: example

            Strings II and III:

            >>> indicator = abjad.StringNumber((2, 3))
            >>> indicator.roman_numerals
            ('ii', 'iii')

        '''
        numerals = ('i', 'ii', 'iii', 'iv', 'v', 'vi')
        result = []
        for number in self.numbers:
            numeral = numerals[number - 1]
            result.append(numeral)
        return tuple(result)
