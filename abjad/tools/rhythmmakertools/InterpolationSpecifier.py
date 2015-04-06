# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class InterpolationSpecifier(AbjadValueObject):
    r'''Interpolation specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_duration',
        '_stop_duration',
        '_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_duration=durationtools.Duration(1, 8),
        stop_duration=durationtools.Duration(1, 16),
        written_duration=durationtools.Duration(1, 16),
        ):
        self._start_duration = durationtools.Duration(start_duration)
        self._stop_duration = durationtools.Duration(stop_duration)
        self._written_duration = durationtools.Duration(written_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def start_duration(self):
        r'''Gets start duration of interpolation specifier.

        Defaults to ``1/8``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._start_duration

    @property
    def stop_duration(self):
        r'''Gets stop duration of interpolation specifier.

        Defaults to ``1/16``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._stop_duration

    @property
    def written_duration(self):
        r'''Gets written duration of interpolation specifier.

        Defaults to ``1/16``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._written_duration