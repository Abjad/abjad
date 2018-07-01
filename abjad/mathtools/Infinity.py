from abjad.system.AbjadValueObject import AbjadValueObject


class Infinity(AbjadValueObject):
    """
    Infinity.

    ..  container:: example

        All numbers compare less than infinity:

        >>> 9999999 < Infinity
        True

        >>> 2**38 < Infinity
        True

    ..  container:: example

        Infinity compares equal to itself:

        >>> Infinity == Infinity
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> NegativeInfinity < Infinity
        True

    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad starts.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_value',
        )

    ### INTIALIZER ###

    def __init__(self):
        self._value = float('infinity')

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is also infinity.

        Returns true or false.
        """
        return super().__eq__(argument)

    def __float__(self):
        """
        Convert infinity to float.

        Returns float.
        """
        return self._value

    def __ge__(self, argument):
        """
        Is true for all values of ``argument``.

        Returns true.
        """
        return self._value >= argument

    def __gt__(self, argument):
        """
        Is true for all noninfinite values of ``argument``.

        Returns true or false.
        """
        return self._value > argument

    def __hash__(self):
        """
        Hashes infinity.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __le__(self, argument):
        """
        Is true when ``argument`` is infinite.

        Returns true or false.
        """
        return self._value <= argument

    def __lt__(self, argument):
        """
        Is true for no values of ``argument``.

        Returns true or false.
        """
        return self._value < argument

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from infinity.

        Returns infinity or 0 if ``argument`` is also infinity.
        """
        if argument is self:
            return 0
        return self

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad import system
        return system.FormatSpecification(
            client=self,
            repr_text=type(self).__name__,
            storage_format_text=type(self).__name__,
            )
