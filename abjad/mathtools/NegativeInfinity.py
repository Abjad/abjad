from .Infinity import Infinity


class NegativeInfinity(Infinity):
    """
    Negative infinity.

    ..  container:: example

        All numbers compare greater than negative infinity:

        >>> NegativeInfinity < -9999999
        True

    ..  container:: example

        Negative infinity compares equal to itself:

        >>> NegativeInfinity == NegativeInfinity
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> NegativeInfinity < Infinity
        True

    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad start.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        self._value = float('-infinity')
