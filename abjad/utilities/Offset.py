from .Duration import Duration


class Offset(Duration):
    """
    Offset.

    ..  container:: example

        Initializes from integer numerator:

        >>> abjad.Offset(3)
        Offset(3, 1)

    ..  container:: example

        Initializes from integer numerator and denominator:

        >>> abjad.Offset(3, 16)
        Offset(3, 16)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator:

        >>> abjad.Offset(3.0)
        Offset(3, 1)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator and denominator:

        >>> abjad.Offset(3.0, 16)
        Offset(3, 16)

    ..  container:: example

        Initializes from integer-equivalent singleton:

        >>> abjad.Offset((3,))
        Offset(3, 1)

    ..  container:: example

        Initializes from integer-equivalent pair:

        >>> abjad.Offset((3, 16))
        Offset(3, 16)

    ..  container:: example

        Initializes from duration:

        >>> abjad.Offset(abjad.Duration(3, 16))
        Offset(3, 16)

    ..  container:: example

        Initializes from other offset:

        >>> abjad.Offset(abjad.Offset(3, 16))
        Offset(3, 16)

    ..  container:: example

        Initializes from other offset with grace displacement:

        >>> offset = abjad.Offset((3, 16), grace_displacement=(-1, 16))
        >>> abjad.Offset(offset)
        Offset(
            (3, 16),
            grace_displacement=Duration(-1, 16)
            )

    ..  container:: example

        Intializes from fraction:

        >>> abjad.Offset(abjad.Fraction(3, 16))
        Offset(3, 16)

    ..  container:: example

        Initializes from solidus string:

        >>> abjad.Offset('3/16')
        Offset(3, 16)

    ..  container:: example

        Initializes from nonreduced fraction:

        >>> abjad.Offset(abjad.NonreducedFraction(6, 32))
        Offset(3, 16)

    ..  container:: example

        Offsets inherit from built-in fraction:

        >>> isinstance(abjad.Offset(3, 16), abjad.Fraction)
        True

    ..  container:: example

        Offsets are numbers:

        >>> import numbers

        >>> isinstance(abjad.Offset(3, 16), numbers.Number)
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_grace_displacement',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments, **keywords):
        grace_displacement = None
        for argument in arguments:
            try:
                grace_displacement = argument.grace_displacement
                break
            except AttributeError:
                pass
        grace_displacement = grace_displacement or keywords.get(
            'grace_displacement')
        if grace_displacement is not None:
            grace_displacement = Duration(grace_displacement)
        grace_displacement = grace_displacement or None
        if len(arguments) == 1 and isinstance(arguments[0], Duration):
            arguments = arguments[0].pair
        self = Duration.__new__(class_, *arguments)
        self._grace_displacement = grace_displacement
        return self

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Copies offset.

        >>> import copy

        ..  container:: example

            Copies offset with grace displacement:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = copy.copy(offset_1)

            >>> offset_1
            Offset(
                (1, 4),
                grace_displacement=Duration(-1, 16)
                )

            >>> offset_2
            Offset(
                (1, 4),
                grace_displacement=Duration(-1, 16)
                )

            >>> offset_1 == offset_2
            True

            >>> offset_1 is offset_2
            False

        Returns new offset.
        """
        return type(self)(
            self.pair,
            grace_displacement=self.grace_displacement
            )

    def __deepcopy__(self, *arguments):
        """
        Deep copies offset.

        >>> import copy

        ..  container:: example

            Copies offset with grace displacement:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = copy.deepcopy(offset_1)

            >>> offset_1
            Offset(
                (1, 4),
                grace_displacement=Duration(-1, 16)
                )

            >>> offset_2
            Offset(
                (1, 4),
                grace_displacement=Duration(-1, 16)
                )

            >>> offset_1 == offset_2
            True

            >>> offset_1 is offset_2
            False

        Returns new offset.
        """
        return self.__copy__(*arguments)

    def __eq__(self, argument):
        """
        Is true when offset equals ``argument``.

        ..  container:: example

            With equal numerators, denominators and grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            True
            >>> offset_2 == offset_1
            True
            >>> offset_2 == offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            False
            >>> offset_2 == offset_1
            False
            >>> offset_2 == offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), grace_displacement=(-99))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            False
            >>> offset_2 == offset_1
            False
            >>> offset_2 == offset_2
            True

        Returns true or false.
        """
        if isinstance(argument, type(self)) and self.pair == argument.pair:
            return self._get_grace_displacement() == \
                argument._get_grace_displacement()
        return super().__eq__(argument)

    def __ge__(self, argument):
        """
        Is true when offset is greater than or equal to ``argument``.

        ..  container:: example

            With equal numerators, denominators and grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            True
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            False
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), grace_displacement=(-99))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            False
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        Returns true or false.
        """
        if isinstance(argument, type(self)) and self.pair == argument.pair:
            return self._get_grace_displacement() >= \
                argument._get_grace_displacement()
        return super().__ge__(argument)

    def __gt__(self, argument):
        """
        Is true when offset is greater than ``argument``.

        ..  container:: example

            With equal numerators, denominators and grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            False
            >>> offset_2 > offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            True
            >>> offset_2 > offset_2
            False

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), grace_displacement=(-99))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            True
            >>> offset_2 > offset_2
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)) and self.pair == argument.pair:
            return self._get_grace_displacement() > \
                argument._get_grace_displacement()
        return Duration.__gt__(self, argument)

    def __hash__(self):
        """
        Hashes offset.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __le__(self, argument):
        """
        Is true when offset is less than or equal to ``argument``.

        ..  container:: example

            With equal numerators, denominators and grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            True
            >>> offset_2 <= offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            False
            >>> offset_2 <= offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), grace_displacement=(-99))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            False
            >>> offset_2 <= offset_2
            True

        Returns true or false.
        """
        if isinstance(argument, type(self)) and self.pair == argument.pair:
            return self._get_grace_displacement() <= \
                argument._get_grace_displacement()
        return super().__le__(argument)

    def __lt__(self, argument):
        """
        Is true when offset is less than ``argument``.

        ..  container:: example

            With equal numerators, denominators and grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            False
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing nonzero grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), grace_displacement=(-1, 16))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing zero-valued
            grace displacements:

            >>> offset_1 = abjad.Offset((1, 4), grace_displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), grace_displacement=(-99))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)) and self.pair == argument.pair:
            return self._get_grace_displacement() < \
                argument._get_grace_displacement()
        return super().__lt__(argument)

    def __repr__(self):
        """
        Gets interpreter representation of offset.

        ..  container:: example

            Gets interpreter representation of offset without grace
            displacement:

            >>> abjad.Offset(1, 4)
            Offset(1, 4)

        ..  container:: example

            Gets interpreter representation of offset with grace displacement:

            >>> abjad.Offset(1, 4, grace_displacement=(-1, 16))
            Offset(
                (1, 4),
                grace_displacement=Duration(-1, 16)
                )

        """
        return super().__repr__()

    def __sub__(self, argument):
        """
        Offset taken from offset returns duration:

        >>> abjad.Offset(2) - abjad.Offset(1, 2)
        Duration(3, 2)

        Duration taken from offset returns another offset:

        >>> abjad.Offset(2) - abjad.Duration(1, 2)
        Offset(3, 2)

        Coerce ``argument`` to offset when ``argument`` is neither offset nor
        duration:

        >>> abjad.Offset(2) - abjad.Fraction(1, 2)
        Duration(3, 2)

        Returns duration or offset.
        """
        if isinstance(argument, type(self)):
            return Duration(super().__sub__(argument))
        elif isinstance(argument, Duration):
            return super().__sub__(argument)
        else:
            argument = type(self)(argument)
            return self - argument

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.system.FormatSpecification import \
            FormatSpecification
        is_indented = False
        names = []
        values = [self.numerator, self.denominator]
        if self._get_grace_displacement():
            is_indented = True
            names = ['grace_displacement']
            values = [(self.numerator, self.denominator)]
        return FormatSpecification(
            client=self,
            repr_is_indented=is_indented,
            storage_format_args_values=values,
            storage_format_is_indented=is_indented,
            storage_format_kwargs_names=names,
            )

    def _get_grace_displacement(self):
        import abjad
        if self.grace_displacement is None:
            return abjad.Duration(0)
        return self.grace_displacement

    ### PUBLIC PROPERTIES ###

    @property
    def grace_displacement(self):
        """
        Gets grace displacement.

        ..  container:: example

            Gets grace displacement equal to none:

            >>> offset = abjad.Offset(1, 4)
            >>> offset.grace_displacement is None
            True

        ..  container:: example

            Gets grace displacement equal to a negative sixteenth:

            >>> offset = abjad.Offset(1, 4, grace_displacement=(-1, 16))
            >>> offset.grace_displacement
            Duration(-1, 16)

        ..  container:: example

            Stores zero-valued grace displacement as none:

            >>> offset = abjad.Offset(1, 4, grace_displacement=0)
            >>> offset.grace_displacement is None
            True

            >>> offset
            Offset(1, 4)

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        """
        return self._grace_displacement
