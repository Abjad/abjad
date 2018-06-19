from .Inequality import Inequality


class LengthInequality(Inequality):
    """
    Length inequality.

    ..  container:: example

        >>> inequality = abjad.LengthInequality('<', 4)
        >>> abjad.f(inequality)
        abjad.LengthInequality(
            operator_string='<',
            length=4,
            )

        >>> inequality([1, 2, 3])
        True

        >>> inequality([1, 2, 3, 4])
        False

        >>> inequality([1, 2, 3, 4, 5])
        False

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_length',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string='<',
        length=None,
        ):
        import abjad
        Inequality.__init__(self, operator_string=operator_string)
        if length is None:
            length = abjad.mathtools.Infinity()
        assert 0 <= length
        infinities = (
            abjad.mathtools.Infinity(),
            abjad.mathtools.NegativeInfinity(),
            )
        if length not in infinities:
            length = int(length)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        return self._operator_function(len(argument), self.length)

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        """
        Gets length.

        Returns integer.
        """
        return self._length
