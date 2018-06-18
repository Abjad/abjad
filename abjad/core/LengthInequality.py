import typing
from abjad import mathtools
from abjad import typings
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
        operator_string: str = '<',
        length: typing.Union[int, typings.Infinities] = None,
        ) -> None:
        Inequality.__init__(self, operator_string=operator_string)
        if length is None:
            length = mathtools.Infinity()
        prototype = (
            int,
            mathtools.Infinity,
            mathtools.NegativeInfinity,
            )
        assert isinstance(length, prototype), repr(length)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        return self._operator_function(len(argument), self.length)

    ### PUBLIC PROPERTIES ###

    @property
    def length(self) -> typing.Union[int, typings.Infinities]:
        """
        Gets length.
        """
        return self._length
