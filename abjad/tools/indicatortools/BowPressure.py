# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class BowPressure(AbjadObject):
    r'''Bow pressure indicator.

    ::

        >>> indicator = indicatortools.BowPressure('overpressure')
        >>> print(format(indicator))
        indicatortools.BowPressure(
            pressure='overpressure',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pressure',
        )

    ### INITIALIZER ###

    def __init__(self,
        pressure=None,
        ):
        self._pressure = pressure

    ### PUBLIC PROPERTIES ###

    @property
    def pressure(self):
        r'''Gets pressure.

        ::

            >>> indicator = indicatortools.BowPressure('underpressure')
            >>> indicator.pressure
            'underpressure'

        '''
        return self._pressure
