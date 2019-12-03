import typing

from abjad.mathtools import Infinity, NegativeInfinity

from .Duration import Duration
from .Inequality import Inequality


class DurationInequality(Inequality):
    """
    Duration inequality.

    ..  container:: example

        >>> inequality = abjad.DurationInequality('<', (3, 4))
        >>> abjad.f(inequality)
        abjad.DurationInequality(
            operator_string='<',
            duration=abjad.Duration(3, 4),
            )

        >>> inequality(abjad.Duration(1, 2))
        True

        >>> inequality(abjad.Note("c'4"))
        True

        >>> inequality(abjad.Container("c'1 d'1"))
        False

    ..  container:: example

        Has clean interpreter representation:

        >>> abjad.DurationInequality('<', (3, 4))
        DurationInequality(operator_string='<', duration=Duration(3, 4))

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_duration", "_preprolated")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self, operator_string: str = "<", duration=None, *, preprolated: bool = None,
    ) -> None:
        Inequality.__init__(self, operator_string=operator_string)
        if duration is None:
            duration = Infinity()
        infinities = (Infinity(), NegativeInfinity())
        if duration not in infinities:
            duration = Duration(duration)
            assert 0 <= duration
        self._duration = duration
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        import abjad

        if isinstance(argument, abjad.Component):
            if self.preprolated:
                duration = argument._get_preprolated_duration()
            else:
                duration = abjad.inspect(argument).duration()
        elif isinstance(argument, abjad.Selection):
            if self.preprolated:
                duration = argument._get_preprolated_duration()
            else:
                duration = abjad.inspect(argument).duration()
        else:
            duration = abjad.Duration(argument)
        return self._operator_function(duration, self.duration)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> Duration:
        """
        Gets duration.
        """
        return self._duration

    @property
    def preprolated(self) -> typing.Optional[bool]:
        """
        Is true when inequality evaluates preprolated duration.
        """
        return self._preprolated
