# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class BowPressure(AbjadObject):
    r'''Bow pressure.

    ..  container:: example

        ::

            >>> bow_pressure = indicatortools.BowPressure('overpressure')
            >>> print(format(bow_pressure))
            indicatortools.BowPressure(
                pressure='overpressure',
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pressure',
        )

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

            ::

                >>> bow_pressure = indicatortools.BowPressure('underpressure')
                >>> bow_pressure.pressure
                'underpressure'

        Returns string.
        '''
        return self._pressure