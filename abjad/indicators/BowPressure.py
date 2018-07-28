import typing
from abjad.system.AbjadValueObject import AbjadValueObject


class BowPressure(AbjadValueObject):
    """
    Bow pressure indicator.

    ..  container:: example

        >>> bow_pressure = abjad.BowPressure('overpressure')
        >>> abjad.f(bow_pressure)
        abjad.BowPressure(
            pressure='overpressure',
            )

        >>> bow_pressure = abjad.BowPressure('underpressure')
        >>> abjad.f(bow_pressure)
        abjad.BowPressure(
            pressure='underpressure',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pressure',
        )

    _parameter = True

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, pressure: str = None) -> None:
        self._pressure = pressure

    ### PUBLIC PROPERTIES ###

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.BowPressure('overpressure').parameter
            True

        """
        return self._parameter

    @property
    def pressure(self) -> typing.Optional[str]:
        """
        Gets pressure of indicator.

        ..  container:: example

            Overpressure:

            >>> bow_pressure = abjad.BowPressure('overpressure')
            >>> bow_pressure.pressure
            'overpressure'

        ..  container:: example

            Underpressure:

            >>> bow_pressure = abjad.BowPressure('underpressure')
            >>> bow_pressure.pressure
            'underpressure'

        """
        return self._pressure

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on bow pressure.
        """
        pass
