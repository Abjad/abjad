from .NumberedIntervalClass import NumberedIntervalClass


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    """
    Numbered inversion-equivalent interval-class.

    ..  container:: example

        Initializes from integer:

        >>> abjad.NumberedInversionEquivalentIntervalClass(0)
        NumberedInversionEquivalentIntervalClass(0)

        >>> abjad.NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(1)

    ..  container:: example

        Initializes from float:

        >>> abjad.NumberedInversionEquivalentIntervalClass(1.5)
        NumberedInversionEquivalentIntervalClass(1.5)

    ..  container:: example

        Initializes from string:

        >>> abjad.NumberedInversionEquivalentIntervalClass('1')
        NumberedInversionEquivalentIntervalClass(1)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, number=0):
        super().__init__(number or 0)
        self._number %= 12
        if 6 < self._number:
            self._number = 12 - self._number

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(0))
            NumberedInversionEquivalentIntervalClass(0)

            >>> abs(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(abs(self.number))

    def __lt__(self, argument):
        """
        Is true when `argument` is a numbered inversion-equivalent
        interval-class with a number less than this numbered
        inversion-equivalent interval-class.
        """
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self):
        """
        Negates numbered inversion-equivalent interval-class.

        ..  container:: example

            >>> -abjad.NumberedInversionEquivalentIntervalClass(0)
            NumberedInversionEquivalentIntervalClass(0)

            >>> -abjad.NumberedInversionEquivalentIntervalClass(1.5)
            NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        """
        return type(self)(self.number)

    def __str__(self):
        """
        Gets string representation of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(0))
            '0'

            >>> str(abjad.NumberedInversionEquivalentIntervalClass(1.5))
            '1.5'

        Returns string.
        """
        return str(self.number)
