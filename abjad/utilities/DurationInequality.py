import typing

from .. import mathtools
from ..duration import Duration
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
            duration = mathtools.Infinity()
        infinities = (mathtools.Infinity(), mathtools.NegativeInfinity())
        if duration not in infinities:
            duration = Duration(duration)
            assert 0 <= duration
        self._duration = duration
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        from ..core.Component import inspect

        if self.preprolated and hasattr(argument, "_get_preprolated_duration"):
            duration = argument._get_preprolated_duration()
        else:
            try:
                duration = inspect(argument).duration()
            except TypeError:
                duration = Duration(argument)
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
