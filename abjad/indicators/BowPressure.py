import typing

from .. import format as _format


class BowPressure:
    """
    Bow pressure indicator.

    ..  container:: example

        >>> bow_pressure = abjad.BowPressure('overpressure')
        >>> string = abjad.storage(bow_pressure)
        >>> print(string)
        abjad.BowPressure(
            pressure='overpressure',
            )

        >>> bow_pressure = abjad.BowPressure('underpressure')
        >>> string = abjad.storage(bow_pressure)
        >>> print(string)
        abjad.BowPressure(
            pressure='underpressure',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_pressure",)

    _parameter = "BOW_PRESSURE"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, pressure: str = None) -> None:
        self._pressure = pressure

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes bow pressure.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def parameter(self) -> str:
        """
        Returns ``'BOW_PRESSURE'``.

        ..  container:: example

            >>> abjad.BowPressure('overpressure').parameter
            'BOW_PRESSURE'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.BowPressure('overpressure').persistent
            True

        """
        return self._persistent

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
