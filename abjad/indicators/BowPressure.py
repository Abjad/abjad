import typing

from ..storage import StorageFormatManager


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
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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
