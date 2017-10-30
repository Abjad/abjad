from abjad.tools.abctools import AbjadValueObject


class BowPressure(AbjadValueObject):
    r'''Bow pressure indicator.

    ..  container:: example

        Overpressure indicator:

        ..  container:: example

            >>> bow_pressure = abjad.BowPressure('overpressure')
            >>> abjad.f(bow_pressure)
            abjad.BowPressure(
                pressure='overpressure',
                )

    ..  container:: example

        Underpressure indicator:

        ..  container:: example

            >>> bow_pressure = abjad.BowPressure('underpressure')
            >>> abjad.f(bow_pressure)
            abjad.BowPressure(
                pressure='underpressure',
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pressure',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pressure=None,
        ):
        self._pressure = pressure

    ### PUBLIC PROPERTIES ###

    @property
    def pressure(self):
        r'''Gets pressure of indicator.

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

        Returns string.
        '''
        return self._pressure
