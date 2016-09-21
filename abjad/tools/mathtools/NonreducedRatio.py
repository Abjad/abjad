# -*- coding: utf-8 -*-
import collections
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class NonreducedRatio(AbjadValueObject):
    '''Nonreduced ratio.

    ..  container:: example

        **Example 1.** Nonreduced ratio of two numbers:

        ::

            >>> mathtools.NonreducedRatio((2, 4))
            NonreducedRatio((2, 4))

    ..  container:: example

        **Example 2.** Nonreduced ratio of three numbers:

            >>> mathtools.NonreducedRatio((2, 4, 2))
            NonreducedRatio((2, 4, 2))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        numbers = tuple(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''Is true when ratio contains `expr`. Otherwise false.

        Returns true or false.
        '''
        return expr in self._numbers

    def __eq__(self, expr):
        r'''Is true when `expr` is a nonreduced ratio with numerator and
        denominator equal to those of this nonreduced ratio. Otherwise false.

        Returns true or false.
        '''
        if not isinstance(expr, type(self)):
            return False
        expr = type(self)(expr)
        return self.numbers == expr.numbers

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> print(format(ratio))
                mathtools.NonreducedRatio((2, 4, 2))

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getitem__(self, i):
        r'''Gets item at `i`.

        ..  container:: example

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> ratio[1]
                4

        Returns integer or tuple.
        '''
        if isinstance(i, slice):
            return tuple(self._numbers[i])
        return self._numbers[i]

    def __hash__(self):
        r'''Hashes non-reduced ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NonreducedRatio, self).__hash__()

    def __iter__(self):
        r'''Iterates ratio.

        Returns generator.
        '''
        return iter(self._numbers)

    def __len__(self):
        r'''Gets length of ratio.

        ..  container:: example

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> len(ratio)
                3

        Returns integer.
        '''
        return len(self._numbers)

    def __reversed__(self):
        r'''Iterates ratio in reverse.

        Returns generator.
        '''
        return reversed(self._numbers)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=[self.numbers],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC METHODS ###

    def count(self, expr):
        r'''Gets count of `expr` in ratio.

        Returns integer.
        '''
        return self._numbers.count(expr)

    def index(self, expr):
        r'''Gets index of `expr` in ratio.

        Returns integer.
        '''
        return self._numbers.index(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _number_coercer(self):
        return int

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        r'''Gets multipliers of nonreduced ratio.

        ..  container:: example

            **Example 1.** Nonreduced ratio of two numbers:

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4))
                >>> ratio.multipliers
                (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            **Example 2.** Nonreduced ratio of three numbers:

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> ratio.multipliers
                (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        '''
        from abjad.tools import durationtools
        weight = sum(self.numbers)
        multipliers = [
            durationtools.Multiplier((_, weight))
            for _ in self.numbers
            ]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        r'''Gets numbers of nonreduced ratio.

        ..  container:: example

            **Example 1.** Nonreduced ratio of two numbers:

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4))
                >>> ratio.numbers
                (2, 4)

        ..  container:: example

            **Example 2.** Nonreduced ratio of three numbers:

            ::

                >>> ratio = mathtools.NonreducedRatio((2, 4, 2))
                >>> ratio.numbers
                (2, 4, 2)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        '''
        return self._numbers


collections.Sequence.register(NonreducedRatio)
