import typing
from abjad import mathtools
from abjad import typings
from abjad.utilities.Duration import Duration
from abjad.top.inspect import inspect
from .Component import Component
from .Inequality import Inequality
from .Selection import Selection


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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_duration',
        '_preprolated',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string: str = '<',
        duration: typing.Union[
            Duration,
            typings.Infinities,
            typings.IntegerPair,
            ] = None,
        *,
        preprolated: bool = None,
        ) -> None:
        Inequality.__init__(self, operator_string=operator_string)
        if duration is None:
            duration = mathtools.Infinity()
        infinities = (
            mathtools.Infinity(),
            mathtools.NegativeInfinity(),
            )
        if duration not in infinities:
            duration = Duration(duration)
            assert 0 <= duration
        prototype = (
            Duration,
            mathtools.Infinity,
            mathtools.NegativeInfinity,
            )
        assert isinstance(duration, prototype)
        self._duration = duration
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> bool:
        """
        Calls inequality on ``argument``.
        """
        if isinstance(argument, Component):
            if self.preprolated:
                duration = argument._get_preprolated_duration()
            else:
                duration = inspect(argument).get_duration()
        elif isinstance(argument, Selection):
            if self.preprolated:
                duration = argument._get_preprolated_duration()
            else:
                duration = inspect(argument).get_duration()
        else:
            duration = Duration(argument)
        return self._operator_function(duration, self.duration)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> typing.Union[Duration, typings.Infinities]:
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
