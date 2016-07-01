# -*- coding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Offset(Duration):
    '''Offset.

    ..  container:: example

        **Example 1.** Initializes from integer numerator:

        ::

            >>> Offset(3)
            Offset(3, 1)

    ..  container:: example

        **Example 2.** Initializes from integer numerator and denominator:

        ::

            >>> Offset(3, 16)
            Offset(3, 16)

    ..  container:: example

        **Example 3.** Initializes from integer-equivalent numeric numerator:

        ::

            >>> Offset(3.0)
            Offset(3, 1)

    ..  container:: example

        **Example 4.** Initializes from integer-equivalent numeric numerator
        and denominator:

        ::

            >>> Offset(3.0, 16)
            Offset(3, 16)

    ..  container:: example

        **Example 5.** Initializes from integer-equivalent singleton:

        ::

            >>> Offset((3,))
            Offset(3, 1)

    ..  container:: example

        **Example 6.** Initializes from integer-equivalent pair:

        ::

            >>> Offset((3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 7.** Initializes from duration:

        ::

            >>> Offset(Duration(3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 8.** Initializes from other offset:

        ::

            >>> Offset(Offset(3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 9.** Initializes from other offset with grace displacement:

        ::

            >>> offset = Offset((3, 16), grace_displacement=(-1, 16))
            >>> Offset(offset)
            Offset((3, 16), grace_displacement=Duration(-1, 16))

    ..  container:: example

        **Example 10.** Intializes from fraction:

        ::

            >>> Offset(Fraction(3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 11.** Initializes from solidus string:

        ::

            >>> Offset('3/16')
            Offset(3, 16)

    ..  container:: example

        **Example 12.** Initializes from nonreduced fraction:

        ::

            >>> Offset(mathtools.NonreducedFraction(6, 32))
            Offset(3, 16)

    ..  container:: example

        **Example 13.** Offsets inherit from built-in fraction:

        ::

            >>> isinstance(Offset(3, 16), Fraction)
            True

    ..  container:: example

        **Example 14.** Offsets are numeric:

        ::

            >>> import numbers

        ::

            >>> isinstance(Offset(3, 16), numbers.Number)
            True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_grace_displacement',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *args, **kwargs):
        self = Duration.__new__(class_, *args)
        grace_displacement = None
        for arg in args:
            if hasattr(arg, 'grace_displacement'):
                grace_displacement = getattr(arg, 'grace_displacement')
                break
        grace_displacement = grace_displacement or kwargs.get(
            'grace_displacement')
        if grace_displacement is not None:
            grace_displacement = Duration(grace_displacement)
        self._grace_displacement = grace_displacement
        return self

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        if self.grace_displacement is None:
            return systemtools.StorageFormatSpecification(
                self,
                is_indented=False,
                positional_argument_values=self.pair,
                keyword_argument_names=(),
                )
        else:
            return systemtools.StorageFormatSpecification(
                self,
                is_indented=False,
                positional_argument_values=(self.pair,),
                keyword_argument_names=('grace_displacement',),
                )

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies offset.

        ::

            >>> import copy

        ..  container:: example

            **Example 1.** Copies offset with grace displacement:

            ::

                >>> offset_1 = Offset((1, 4), grace_displacement=(-1, 16))
                >>> offset_2 = copy.copy(offset_1)

            ::

                >>> offset_1
                Offset((1, 4), grace_displacement=Duration(-1, 16))

            ::

                >>> offset_2
                Offset((1, 4), grace_displacement=Duration(-1, 16))

            ::

                >>> offset_1 == offset_2
                True

        Returns new offset.
        '''
        arguments = self.__getnewargs__()
        return type(self)(
            *arguments,
            grace_displacement=self.grace_displacement
            )

    def __deepcopy__(self, *args):
        r'''Deep copies offset.

        ::

            >>> import copy

        ..  container:: example

            **Example 1.** Copies offset with grace displacement:

            ::

                >>> offset_1 = Offset((1, 4), grace_displacement=(-1, 16))
                >>> offset_2 = copy.deepcopy(offset_1)

            ::

                >>> offset_1
                Offset((1, 4), grace_displacement=Duration(-1, 16))

            ::

                >>> offset_2
                Offset((1, 4), grace_displacement=Duration(-1, 16))

            ::

                >>> offset_1 == offset_2
                True

        Returns new offset.
        '''
        return self.__copy__(*args)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return self.pair

    def __repr__(self):
        r'''Gets interpreter representation of offset.

        ..  container:: example

            **Example 1.** Gets interpreter representation of offset without
            grace displacement:

            ::

                >>> Offset(1, 4)
                Offset(1, 4)

        ..  container:: example

            **Example 2.** Gets interpreter representation of offset with
            grace displacement:

            ::

                >>> Offset(1, 4, grace_displacement=(-1, 16))
                Offset((1, 4), grace_displacement=Duration(-1, 16))

        '''
        return Duration.__repr__(self)

    def __sub__(self, expr):
        '''Offset taken from offset returns duration:

        ::

            >>> durationtools.Offset(2) - durationtools.Offset(1, 2)
            Duration(3, 2)

        Duration taken from offset returns another offset:

        ::

            >>> durationtools.Offset(2) - durationtools.Duration(1, 2)
            Offset(3, 2)

        Coerce `expr` to offset when `expr` is neither offset nor duration:

        ::

            >>> durationtools.Offset(2) - Fraction(1, 2)
            Duration(3, 2)

        Returns duration or offset.
        '''
        if isinstance(expr, type(self)):
            return Duration(Duration.__sub__(self, expr))
        elif isinstance(expr, Duration):
            return Duration.__sub__(self, expr)
        else:
            expr = type(self)(expr)
            return self - expr

    ### PUBLIC PROPERTIES ###

    @property
    def grace_displacement(self):
        r'''Gets grace displacement.

        ..  container:: example

            **Example 1.** Gets grace displacement equal to none:

            ::

                >>> offset = Offset(1, 4)
                >>> offset.grace_displacement is None
                True

        ..  container:: example

            **Example 2.** Gets grace displacement equal to a negative
            sixteenth:

            ::

                >>> offset = Offset(1, 4, grace_displacement=(-1, 16))
                >>> offset.grace_displacement
                Duration(-1, 16)

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._grace_displacement