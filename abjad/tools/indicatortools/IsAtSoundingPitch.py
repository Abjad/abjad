# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class IsAtSoundingPitch(AbjadValueObject):
    r'''Sounding pitch indicator.

    ..  container:: example

        ::

            >>> indicator = indicatortools.IsAtSoundingPitch()

    Attach to score selection to denote music written at sounding pitch.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._default_scope = None

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of sounding pitch indicator.

        ..  container:: example

            >>> indicator = indicatortools.IsAtSoundingPitch()
            >>> indicator.default_scope is None
            True

        Returns none.
        '''
        return self._default_scope
