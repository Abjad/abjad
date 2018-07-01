from .NonreducedRatio import NonreducedRatio


class Ratio(NonreducedRatio):
    """
    Ratio.

    ..  container:: example

        Ratio of two numbers:

        >>> abjad.Ratio((2, 4))
        Ratio((1, 2))

    ..  container:: example

        Ratio of three numbers:

        >>> abjad.Ratio((2, 4, 2))
        Ratio((1, 2, 1))

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        import abjad
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        numbers = [int(_) for _ in numbers]
        gcd = abjad.mathtools.greatest_common_divisor(*numbers)
        numbers = [_ // gcd for _ in numbers]
        self._numbers = tuple(numbers)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals ratio.

        ..  container:: example

            >>> ratio_1 = abjad.Ratio((1, 2, 1))
            >>> ratio_2 = abjad.Ratio((1, 2, 1))
            >>> ratio_3 = abjad.Ratio((2, 3, 3))

            >>> ratio_1 == ratio_1
            True

            >>> ratio_1 == ratio_2
            True

            >>> ratio_1 == ratio_3
            False

            >>> ratio_2 == ratio_1
            True

            >>> ratio_2 == ratio_2
            True

            >>> ratio_2 == ratio_3
            False

            >>> ratio_3 == ratio_1
            False

            >>> ratio_3 == ratio_2
            False

            >>> ratio_3 == ratio_3
            True

        """
        return super().__eq__(argument)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio[1]
            2

        Returns integer or tuple.
        """
        if isinstance(argument, slice):
            return tuple(self._numbers.__getitem__(argument))
        return self._numbers.__getitem__(argument)

    def __hash__(self):
        """
        Hashes ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self._numbers)

    def __str__(self):
        """
        Gets string representation of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> str(abjad.Ratio((2, 4)))
            '1:2'

        ..  container:: example

            Ratio of three numbers:

            >>> str(abjad.Ratio((2, 4, 2)))
            '1:2:1'

        Returns string.
        """
        numbers = (str(x) for x in self.numbers)
        return ':'.join(numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        """
        Gets multipliers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.multipliers
            (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.multipliers
            (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        """
        import abjad
        weight = sum(self.numbers)
        multipliers = [
            abjad.Multiplier((_, weight))
            for _ in self.numbers
            ]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        """
        Gets numbers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.numbers
            (1, 2)

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.numbers
            (1, 2, 1)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        """
        return self._numbers

    @property
    def reciprocal(self):
        """
        Gets reciprocal.

        ..  container:: example

            Gets reciprocal:

            >>> abjad.Ratio((3, 2)).reciprocal
            Ratio((2, 3))

            >>> abjad.Ratio((3, 2, 7)).reciprocal
            Ratio((7, 2, 3))

        Returns new ratio.
        """
        numbers = list(reversed(self.numbers))
        return type(self)(numbers)
